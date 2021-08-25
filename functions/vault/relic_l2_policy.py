
import hvac
import os
import sys

# Limits traceback messaging, comment for further issue details 
# sys.tracebacklimit = 0

error="->THERE'S AN ERROR Message:<-"

def func_l2_policy(client, **kwargs):

    try:
        # create policy
        policy_response = client.sys.create_or_update_policy(
            name=kwargs.get('policy_name'), # [shared] tev-L3APMID-shared-ROLE, [relic] relic-L2APMID, [L3] tev-L3APMID-ROLE
            policy=kwargs.get('policy'),
        )
        print(f"\t{kwargs.get('role')} Policy, added!")
        print(f"\t{kwargs.get('policy_name')}")
    except Exception as e:
        print(f'\n{ error }\n' + str(e) + '\n')
        raise

def func_relic_policy(client, **kwargs):

    try:
        policy_status = client.sys.create_or_update_policy(
            name=kwargs.get('policy_name'), # [shared] tev-L3APMID-shared-ROLE, [relic] relic-L2APMID, [L3] tev-L3APMID-ROLE
            policy=kwargs.get('policy'),
        )
        print('\tRelic Policy, added!')
        print(f"\t{kwargs.get('policy_name')}")
    except Exception as e:
        print(f'\n{ error }\n' + str(e) + '\n')
        raise

#----------------
# Execution Time
#----------------
def func_relic_l2_policies(client, **kwargs):

    return_data =dict()
    return_data['relic_policy_name'] =kwargs.get('policy_name')
    return_data['relic_policy'] =kwargs.get('policy')
    # prefix for all policies, internal group
    prefix =kwargs.get('prefix')

    # Relic
    print('\n\tRELIC POLICIES CREATION:')
    func_relic_policy(client, **kwargs)

    # L2 POLICIES
    print('\n\tL2 POLICIES CREATION:')
    return_data['l2_policy_adm_name'] =f"{kwargs.get('prefix')}-{kwargs.get('L2_APMID').lower()}-shared-adm"
    return_data['l2_policy_adm']      =kwargs.get('admin_shared_policy').replace('L2_APMID',kwargs.get('L2_APMID'))

    return_data['l2_policy_rw_name'] =f"{kwargs.get('prefix')}-{kwargs.get('L2_APMID').lower()}-shared-rw"
    return_data['l2_policy_rw']      =kwargs.get('read_write_shared_policy').replace('L2_APMID',kwargs.get('L2_APMID'))

    return_data['L2_policy_ro_name']  =f"{kwargs.get('prefix')}-{kwargs.get('L2_APMID').lower()}-shared-ro"
    return_data['L2_policy_ro']       =kwargs.get('read_only_shared_policy').replace('L2_APMID',kwargs.get('L2_APMID'))

    d_values ={'policy_name': return_data.get('l2_policy_adm_name'), 'policy': return_data.get('l2_policy_adm'), 'role': 'L2 Admin'}
    func_l2_policy(client, **d_values)
    d_values ={'policy_name': return_data.get('l2_policy_rw_name'), 'policy': return_data.get('l2_policy_rw'), 'role': 'L2 Read/Write'}
    func_l2_policy(client, **d_values)
    d_values ={'policy_name': return_data.get('L2_policy_ro_name'), 'policy': return_data.get('L2_policy_ro'), 'role': 'L2 Read Only'}
    func_l2_policy(client, **d_values)

    return return_data
