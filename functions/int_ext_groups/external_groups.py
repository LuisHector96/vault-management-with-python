
import hvac
import os
import sys

# Limits traceback messaging, comment for further issue details 
# sys.tracebacklimit = 0

error="->THERE'S AN ERROR Message:<-"

def func_create_external_group(client, **kwargs):
    """ function to create external groups and alias for AD groups """

    try:
        # create external group
        create_response =client.secrets.identity.create_or_update_group_by_name(
            name=kwargs.get('ext_grp_name'),              # 'oidc_npe_APM0000000_adm' 'okt_npe_APM0000000_adm' 'aad_npe_APM0000000_adm'
            group_type='external',
            policies=kwargs.get('ext_policies'),
            metadata=dict(
                csdm = '{ ' + f"L1 = {kwargs.get('L1_APMID')}, L2 = {kwargs.get('L2_APMID')}" + ' }',
                role = kwargs.get('role') #"read|write|admin"
            ),
        )
        print(f"\n\t{kwargs.get('message')}")
        print(f"\t{kwargs.get('ext_grp_name')}")
        print(f"\tpolicies: {kwargs.get('ext_policies')}")

        # read external group
        read_ext_grp_response = client.secrets.identity.read_group_by_name(
            name=kwargs.get('ext_grp_name'),
        )

        ext_group_id =read_ext_grp_response.get('data').get('id')
        alias_check  =read_ext_grp_response.get('data').get('alias').get('name')
        alias_id     =read_ext_grp_response.get('data').get('alias').get('id')

        # group alias validation
        if alias_check.lower() == kwargs.get('alias_name').lower():
            # update group alias
            client.secrets.identity.update_group_alias(
                entity_id=alias_id,
                name=kwargs.get('alias_name'),
                canonical_id=ext_group_id,
                mount_accessor=kwargs.get('accessor'),
            )

    except hvac.exceptions.InvalidRequest:

        client.secrets.identity.delete_group_by_name(
            name=kwargs.get('ext_grp_name'),
        )

        func_create_external_group(client, **kwargs)

    except AttributeError:
        
        # create alias
        create_response = client.secrets.identity.create_or_update_group_alias(
                name=kwargs.get('alias_name'),
                canonical_id=ext_group_id,
                mount_accessor=kwargs.get('accessor'),
        )
        alias_id = create_response.get('data').get('id')

    except Exception as e:
        print(f'\n{ error }\n' + str(e) + '\n')
        raise
    
    finally:
        return ext_group_id


#----------------
# Execution Time
#----------------
def func_external_groups(client, **kwargs):

    return_data =dict()
    print('\nEXTERNAL GROUPS:')

    # ADMIN
    oidc_ext_group =f"oidc_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_adm".lower()
    okt_ext_group =f"okt_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_adm".lower()
    aad_ext_group =f"aad_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_adm".lower()
    return_data['ext_alias_group_adm'] =f"{kwargs.get('prefix')}_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_adm".lower()
    accessors =kwargs.get('accessors')

    adm_ext_grp_id =dict()
    d_values ={ 'ext_grp_name': oidc_ext_group, 'ext_policies': kwargs.get('ext_policies'), 'L1_APMID': kwargs.get('l1_asset'), 'L2_APMID': kwargs.get('L2_APMID'), 
                'role': 'adm', 'message': 'Admin oidc external group added!',
                'alias_name': return_data.get('ext_alias_group_adm'), 'accessor': accessors.get('oidc_accessor')
                }
    adm_ext_grp_id['oidc'] =func_create_external_group(client, **d_values)

    d_values ={ 'ext_grp_name': okt_ext_group, 'ext_policies': kwargs.get('ext_policies'), 'L1_APMID': kwargs.get('l1_asset'), 'L2_APMID': kwargs.get('L2_APMID'), 
                'role': 'adm', 'message': 'Admin okt external group added!',
                'alias_name': return_data.get('ext_alias_group_adm'), 'accessor': accessors.get('okt_accessor')
                }
    adm_ext_grp_id['okt'] =func_create_external_group(client, **d_values)

    d_values ={ 'ext_grp_name': aad_ext_group, 'ext_policies': kwargs.get('ext_policies'), 'L1_APMID': kwargs.get('l1_asset'), 'L2_APMID': kwargs.get('L2_APMID'), 
                'role': 'adm', 'message': 'Admin aad external group added!',
                'alias_name': return_data.get('ext_alias_group_adm'), 'accessor': accessors.get('aad_accessor')
                }
    adm_ext_grp_id['aad'] =func_create_external_group(client, **d_values)

    return_data['adm_ext_groups']=adm_ext_grp_id

    # READ/WRITE
    oidc_ext_group =f"oidc_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_rw".lower()
    okt_ext_group =f"okt_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_rw".lower()
    aad_ext_group =f"aad_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_rw".lower()
    return_data['ext_alias_group_rw'] =f"{kwargs.get('prefix')}_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_rw".lower()
    accessors =kwargs.get('accessors')

    rw_ext_grp_id =dict()
    d_values ={ 'ext_grp_name': oidc_ext_group, 'ext_policies': kwargs.get('ext_policies'), 'L1_APMID': kwargs.get('l1_asset'), 'L2_APMID': kwargs.get('L2_APMID'), 
                'role': 'rw', 'message': 'Read/Write oidc external group added!',
                'alias_name': return_data.get('ext_alias_group_rw'), 'accessor': accessors.get('oidc_accessor')
                }
    rw_ext_grp_id['oidc'] =func_create_external_group(client, **d_values)

    d_values ={ 'ext_grp_name': okt_ext_group, 'ext_policies': kwargs.get('ext_policies'), 'L1_APMID': kwargs.get('l1_asset'), 'L2_APMID': kwargs.get('L2_APMID'), 
                'role': 'rw', 'message': 'Read/Write okt external group added!',
                'alias_name': return_data.get('ext_alias_group_rw'), 'accessor': accessors.get('okt_accessor')
                }
    rw_ext_grp_id['okt'] =func_create_external_group(client, **d_values)

    d_values ={ 'ext_grp_name': aad_ext_group, 'ext_policies': kwargs.get('ext_policies'), 'L1_APMID': kwargs.get('l1_asset'), 'L2_APMID': kwargs.get('L2_APMID'), 
                'role': 'rw', 'message': 'Read/Write aad external group added!',
                'alias_name': return_data.get('ext_alias_group_rw'), 'accessor': accessors.get('aad_accessor')
                }
    rw_ext_grp_id['aad'] =func_create_external_group(client, **d_values)

    return_data['rw_ext_groups']=rw_ext_grp_id

    # READ ONLY
    oidc_ext_group =f"oidc_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_ro".lower()
    okt_ext_group =f"okt_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_ro".lower()
    aad_ext_group =f"aad_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_ro".lower()
    return_data['ext_alias_group_ro'] =f"{kwargs.get('prefix')}_{kwargs.get('environment')}_{kwargs.get('L2_APMID')}_ro".lower()
    accessors =kwargs.get('accessors')

    ro_ext_grp_id =dict()
    d_values ={ 'ext_grp_name': oidc_ext_group, 'ext_policies': kwargs.get('ext_policies'), 'L1_APMID': kwargs.get('l1_asset'), 'L2_APMID': kwargs.get('L2_APMID'), 
                'role': 'ro', 'message': 'Read Only oidc external group added!',
                'alias_name': return_data.get('ext_alias_group_ro'), 'accessor': accessors.get('oidc_accessor')
                }
    ro_ext_grp_id['oidc'] =func_create_external_group(client, **d_values)

    d_values ={ 'ext_grp_name': okt_ext_group, 'ext_policies': kwargs.get('ext_policies'), 'L1_APMID': kwargs.get('l1_asset'), 'L2_APMID': kwargs.get('L2_APMID'), 
                'role': 'ro', 'message': 'Read Only okt external group added!',
                'alias_name': return_data.get('ext_alias_group_ro'), 'accessor': accessors.get('okt_accessor')
                }
    ro_ext_grp_id['okt'] =func_create_external_group(client, **d_values)

    d_values ={ 'ext_grp_name': aad_ext_group, 'ext_policies': kwargs.get('ext_policies'), 'L1_APMID': kwargs.get('l1_asset'), 'L2_APMID': kwargs.get('L2_APMID'), 
                'role': 'ro', 'message': 'Read Only aad external group added!',
                'alias_name': return_data.get('ext_alias_group_ro'), 'accessor': accessors.get('aad_accessor')
                }
    ro_ext_grp_id['aad'] =func_create_external_group(client, **d_values)

    return_data['ro_ext_groups']=ro_ext_grp_id

    return return_data
