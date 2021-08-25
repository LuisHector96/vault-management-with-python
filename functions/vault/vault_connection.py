
import hvac
import os
import sys

# Limits traceback messaging, comment for further issue details 
# sys.tracebacklimit = 0

error="->THERE'S AN ERROR Message:<-"

def func_auth_vault_validation(client):
    """ function that validates if you have access to the vault """
    auth_ok     ='\nYou are Authenticated'
    auth_not_ok ='\nNot Authenticated'
    auth_else   ='\nSomething went wrong...\n' + 'Please, try again and verify your access token is working\n'

    def func_else(auth_else):
        raise Warning(auth_else)
        # print(auth_else)
        # sys.exit()

    try:
        auth_status =auth_ok if client.is_authenticated() else auth_not_ok if not client.is_authenticated() else func_else(auth_else)
    except:
        print(auth_else)
        raise
    else:
        print(auth_status)

def func_vault_status(client):
    """ function that prints current status of vault """
    try:
        init ='\nVault Initialized: ' + str(client.sys.is_initialized())
        seal ='\nVault Sealed: ' + str(client.sys.is_sealed())
    except Exception as e:
        print(f'\n{ error }\n' + str(e) + '\n')
        raise
    else:
        print(init + seal)


#----------------
# Execution Time
#----------------
def func_vault_connection(client):
    
    func_auth_vault_validation(client)
    func_vault_status(client)
