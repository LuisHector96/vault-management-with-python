
import hvac
import os
import sys

# Limits traceback messaging, comment for further issue details 
# sys.tracebacklimit = 0

error="->THERE'S AN ERROR Message:<-"

def func_auth_vault_accesors(client):
    """ function to retrieve token accessors for specific auth methods """

    return_data =dict()
    try:
        accessors =client.sys.list_auth_methods()
    except Exception as e:
        print(f'\n{ error }\n' + str(e) + '\n')
        raise
    else:
        return_data['ldap_accessor'] =accessors['ldap/']['accessor']
        return_data['oidc_accessor'] =accessors['oidc/']['accessor']
        return_data['cdp_accessor']  =accessors['cdp/']['accessor']
        return_data['okt_accessor']  =accessors['okt/']['accessor']
        return_data['aad_accessor']  =accessors['aad/']['accessor']

        return return_data
