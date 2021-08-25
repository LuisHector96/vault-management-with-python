
import sys
import os
import hvac

# vault
from functions.vault.vault_connection import *
from functions.vault.vault_accessors import *
from functions.vault.vault_read_onboarding_data import *
from functions.vault.vault_reonboard_validation import *
from functions.vault.vault_standard_output import *
#canvas
from functions.canvas.canvas_data_validation import *
# l2 onboarding
from functions.vault.kv_shared_path import *
from functions.vault.relic_l2_policy import *
# l3 onboarding
from functions.vault.kv_project_path import *
from functions.vault.create_policy import *
from functions.jwt_role.create_jwt_role import *
# groups
from functions.int_ext_groups.internal_groups import *
from functions.int_ext_groups.external_groups import *
# email notifications
from functions.notification.relic_email import *
from functions.notification.vault_only_email import *
from functions.notification.security_group_email import *

from variables import *
from policies import *

#---------------------------
# Vault Client - VAULT_ADDR
#---------------------------
# NOTE: needs variables.py to work
client = hvac.Client(
    url=vault_addr,
    token=vault_token,
    # verify=False, # In case you want to run without validating certs 
)

#---------------------------------
# get email & password from vault
#---------------------------------

if namespace.startswith('tmobile/TEQ-AP-SM'):
    
    email_template =vault_template
    if environment == "PRD":

        sender =prd_vault_sender
        email_kv_response = client.secrets.kv.v2.read_secret_version(
            mount_point='admin',
            path='service_accounts',
        )
        email_password =email_kv_response.get('data').get('data').get('SVC_PRD_vault_onbrd')
    elif environment == "NPE":

        sender =npe_vault_sender
        email_kv_response = client.secrets.kv.v2.read_secret_version(
            mount_point='admin',
            path='service_accounts',
        )
        email_password =email_kv_response.get('data').get('data').get('SVC_DEV_vault_onbrd')
    else:

        sender = 0
        email_password = 0
        assert(False), "Environment was not specified, please specify one of the follow values: NPE/PRD"

else:

    email_template =unified_template
    if environment == "PRD":

        sender =prd_relic_sender
        email_kv_response = client.secrets.kv.v2.read_secret_version(
            mount_point='admin',
            path='service_accounts',
        )
        email_password =email_kv_response.get('data').get('data').get('SVC_PRD_relic_onbrd')
    elif environment == "NPE":

        sender =npe_relic_sender
        email_kv_response = client.secrets.kv.v2.read_secret_version(
            mount_point='admin',
            path='service_accounts',
        )
        email_password =email_kv_response.get('data').get('data').get('SVC_DEV_relic_onbrd')
    else:

        sender = 0
        email_password = 0
        assert(False), "Environment was not specified, please specify one of the follow values: NPE/PRD"

#-----------------------
# Main
#-----------------------
# redirect standard output
console = sys.stdout
sys.stdout = f = open(stdout_file, 'w')

try:
    func_vault_connection(client)
    
    accessor_data =func_auth_vault_accesors(client)

    # read onboard data
    d_values={'file_name': onboard_data_file}
    onboard_data =func_read_onboard_data(**d_values)

    l2_domain_teams =onboard_data.get('onboarding').keys()
    for l2_domain_team in l2_domain_teams:

        L2_APMID =onboard_data.get('onboarding').get(l2_domain_team).get('L2_APMID')

        # Gather L3 APMIDs with repo associated with from L2 APMID
        d_values ={ 'L2_APMID': L2_APMID, 'url_l2_asset': url_l2_asset, 'url_l2_owner': url_l2_owner, 
                    'url_l3_asset': url_l3_asset
                    }
        canvas_data =func_canvas(client, **d_values)

        # reonboarding validation
        d_values ={ 'ldap_addr': ldap_addr, 'ldap_user': sender, 'ldap_password': email_password,
                    'ad_group': f'{prefix}_{environment}_{L2_APMID}'.lower(), 'int_grp_name': f'{prefix}_{L2_APMID}'.lower(),
                    'reonboarding_status': REONBOARD
                    }
        reonboard_validation_response =func_reonboard_validation(client, **d_values)

        # send slack notification when new onboarding
        if reonboard_validation_response['new_onboarding']:
            with open('.env', 'w') as reonboard:
                reonboard.write("export slack_notification=true")
        else:
            with open('.env', 'w') as reonboard:
                reonboard.write("export slack_notification=false")

        # onboarding process
        if not reonboard_validation_response['new_onboarding'] and not reonboard_validation_response['re-onboarding']:

            func_close_stdout(console, f, stdout_file)
            # exit function
            print('exiting...\n')
            sys.exit()
        

        # L2 onboarding only
        print(f"\nRUNNING ONBOARDING REQUEST FOR {L2_APMID} L2 ASSET")
        d_values ={ 'L2_APMID': L2_APMID, 'shared_path': f"{L2_APMID}/shared/README", 'shared_secret': 'shared/', 'readme': readme_message}
        func_l2_shared_path(client, **d_values)

        d_values ={ 'prefix': prefix, 'L2_APMID': L2_APMID, 'policy_name': f'relic-{L2_APMID.lower()}', 
                    'policy': Relic_policy.replace('L2_APMID', L2_APMID), 
                    'admin_shared_policy': L2_Policy_adm, 'read_write_shared_policy':L2_Policy_rw, 'read_only_shared_policy': L2_Policy_ro
                    }
        relic_l2_response =func_relic_l2_policies(client, **d_values)

        print('\nREQUEST COMPLETED!\n')

        # shared policies
        l2_policies =dict()
        l2_policies['l2_adm_shared'] =relic_l2_response.get('l2_policy_adm_name')
        l2_policies['l2_rw_shared'] =relic_l2_response.get('l2_policy_rw_name')
        l2_policies['l2_ro_shared'] =relic_l2_response.get('L2_policy_ro_name')

        # tasks for individual L3 APMIDs
        l3_policies =dict()
        l3_policies['adm'] =[]
        l3_policies['rw']  =[]
        l3_policies['ro']  =[]
        l3_policies['pcf']  =[]
        for l3_asset in canvas_data.get('l3_with_repo_list'):

            print(f"\n\tRUNNING ONBOARDING REQUEST FOR {l3_asset.get('id')} L3 ASSET")
            d_values ={ 'l3_asset': l3_asset, 'L2_APMID': L2_APMID, 'project_path': f"{L2_APMID}/{l3_asset.get('id')}"}
            func_project_path(client, **d_values)

            d_values ={ 'prefix': prefix, 'L2_APMID': L2_APMID, 'L3_APMID': l3_asset.get('id'), 'project_path': f"{L2_APMID}/{l3_asset.get('id')}", 
                        'admin_policy': Admin_policy, 'read_write_policy': Read_Write_policy, 'read_only_policy': Read_Only_policy,
                        'policy_pcf_admin': L3_Policy_pcf_adm
                        }
            policies_response =func_policy_roles(client, **d_values)

            l3_policies['adm'].append(policies_response.get('adm_policy_name'))
            l3_policies['rw'].append(policies_response.get('rw_policy_name'))
            l3_policies['ro'].append(policies_response.get('ro_policy_name'))
            l3_policies['pcf'].append(policies_response.get('adm_pcf_policy_name'))

            ro_policies =[
                policies_response.get('ro_policy_name'),
                relic_l2_response.get('L2_policy_ro_name'),
                relic_l2_response.get('relic_policy_name'),
                policies_response.get('adm_pcf_policy_name'),
                'gitlab-global-ro'
            ]
            d_values ={ 'environment': environment, 'repo_id': l3_asset.get('repo_id'), 'read_policies': ro_policies, 'cdp_entity': 'entity_global_gitlab' ,'accessor': accessor_data.get('cdp_accessor')}
            func_jwt_role(client, **d_values)
            
            print('\n\tREQUEST COMPLETED!\n')

        d_values ={ 'environment': environment, 'prefix': prefix, 'accessors': accessor_data, 
                    'ext_policies': [], 'L1_APMID': canvas_data.get('l1_asset'), 'L2_APMID': L2_APMID
                    }
        ext_grp_ids =func_external_groups(client, **d_values)

        int_policies ={**l3_policies, **l2_policies, 'relic': relic_l2_response.get('relic_policy_name')}
        d_values ={ 'prefix': prefix, 'policies': int_policies, 'L2_APMID': L2_APMID, 'external_groups': ext_grp_ids}
        int_grp_data =func_internal_groups(client, **d_values)

        # EMAIL
        print('\n\nEMAIL TEMPLATE GENERATION')

        try:
            if EMAIL_RESEND: 
                sending_status =True # if EMAIL_RESEND set to true, email will be send.
        except NameError:
            sending_status =reonboard_validation_response['new_onboarding'] # if new_onboarding = true, email will be send

        if ('vault' in sender):
            print('sent vault email')
            d_values ={ 'email_subject': vault_email_subject, 'environment': environment, 'sender': sender, 'email_password': email_password, 
                        'L2_APMID': L2_APMID, 'l2_asset_name':canvas_data.get('l2_asset_name'), 'l2_owner': canvas_data.get('l2_owner_email'), 
                        'ad_group_adm': ext_grp_ids.get('ext_alias_group_adm'), 'ad_group_rw': ext_grp_ids.get('ext_alias_group_rw'), 'ad_group_ro': ext_grp_ids.get('ext_alias_group_ro'), 
                        'l3_asset_list': canvas_data.get('l3_asset_list'), 'email_template': email_template, 'sending_status': sending_status
                        }
            func_vault_only_email_templating(**d_values)
        elif ('relic' in sender):
            print('sent relic email')

            d_values ={ 'email_subject': relic_email_subject, 'environment': environment, 'sender': sender, 'email_password': email_password, 
                        'L2_APMID': L2_APMID, 'l2_asset_name':canvas_data.get('l2_asset_name'), 'l2_owner': canvas_data.get('l2_owner_email'), 
                        'ad_group_adm': ext_grp_ids.get('ext_alias_group_adm'), 'ad_group_rw': ext_grp_ids.get('ext_alias_group_rw'), 'ad_group_ro': ext_grp_ids.get('ext_alias_group_ro'), 
                        'l3_asset_list': canvas_data.get('l3_asset_list'), 'email_template': email_template, 'sending_status': sending_status
                        }
            func_unified_email_templating(**d_values)

        # SG requests
        d_values ={ 'email_subject': sg_email_request_subject, 'environment': environment, 'sender': sender, 'email_password': email_password,
                    'L2_APMID': L2_APMID, 'l2_asset_name':canvas_data.get('l2_asset_name'), 'l2_owner_ntid': canvas_data.get('l2_owner_ntid'),
                    'ad_group_adm': ext_grp_ids.get('ext_alias_group_adm'), 'ad_group_rw': ext_grp_ids.get('ext_alias_group_rw'), 'ad_group_ro': ext_grp_ids.get('ext_alias_group_ro'),
                    'email_template': sg_email_file, 'sending_status': sending_status, 'receiver': 'mahesh.gore2@t-mobile.com'
                    }
        func_sg_requests_creation(**d_values)
        
        func_close_stdout(console, f, stdout_file)

except Exception as e:
    func_close_stdout(console, f, stdout_file)
    raise
