import hvac
import ldap
import os, sys

# Limits traceback messaging, comment for further issue details 
# sys.tracebacklimit = 0

error="->THERE'S AN ERROR Message:<-"

def func_ldap_validation(**kwargs):
    """ function to validate AD group exist in Active Directory"""

    try:
        l = ldap.initialize(kwargs.get('ldap_addr'))
        l.simple_bind_s(kwargs.get('ldap_user'), kwargs.get('ldap_password'))
        search_for =l.search_s('OU=SECURE,OU=ServiceNow,OU=Groups,OU=User Accounts,DC=gsm1900,DC=org',ldap.SCOPE_SUBTREE, filterstr=f"CN={kwargs.get('ad_group')}*")
        group =search_for[0][1].get('cn')
        return True
    except ldap.NO_SUCH_OBJECT:
        # assert(False), 'no group found'
        return False
    except Exception as e:
        print('Error Message:\n' + str(e))
        

def func_internal_groups_existence_validation(client, **kwargs):
    """ function to validate internal groups creation"""

    int_grp_adm =f"{kwargs.get('int_grp_name')}_adm"

    try:
        read_response = client.secrets.identity.read_group_by_name(
                name=int_grp_adm
            )

        message='Internal group found! L3 asset already onboarded'
        status=True
    except:
        message='No match for internal group'
        status=False
    return status

#----------------
# Execution Time
#----------------

def func_reonboard_validation(client, **kwargs):

    return_data =dict()
    return_data['re-onboarding']  =False
    return_data['new_onboarding'] =False

    print('\n- LDAP validation for AD groups -')
    ldap_validation_response =func_ldap_validation(**kwargs)
    if ldap_validation_response:
        print("AD group was found!")
        if kwargs.get('reonboarding_status'):
            print('REONBOARD variable is set to True, proceeding with reonboarding...')
            return_data['re-onboarding'] =True
        else:
            print('REONBOARD variable is set to False\nIf you want to re-onboard, set REONBOARD variable to true:\n\texport REONBOARD=true\n')
            print('Exiting...')
            return_data['re-onboarding'] =False
    else:
        print('- LDAP validation did not found any group, proceeding to internal group validation -')
        int_grp_validation_response =func_internal_groups_existence_validation(client, **kwargs)
        if int_grp_validation_response:
            print("Internal group was found!")
            if kwargs.get('reonboarding_status'):
                print('REONBOARD variable is set to True, proceeding with reonboarding...')
                return_data['re-onboarding'] =True
            else:
                print('REONBOARD variable is set to False\nIf you want to re-onboard, set REONBOARD variable to true:\n\texport REONBOARD=true\n')
                print('Exiting...')
                return_data['re-onboarding'] =False
        else:
            print('No pre-onboarding found, proceeding with regular onboarding...\n')
            return_data['new_onboarding'] =True
    return return_data
