
import hvac
import os
import sys

# Limits traceback messaging, comment for further issue details 
# sys.tracebacklimit = 0

error="->THERE'S AN ERROR Message:<-"

def func_project_path(client, **kwargs):
    """ function to create secret path for specific deployable unit """

    print('\n\t\tPATH CREATION:')
    # check if project path already created or not
    try:
        # list all keypaths in the specific path
        list_response = client.secrets.kv.v2.list_secrets(
            path=kwargs.get('L2_APMID'),
            mount_point='tmobile'
        )
        # validate list_key is in list of keypaths
        if f"{kwargs.get('l3_asset').get('id')}/" in list_response['data']['keys']:
            print('\t\tPath already exist, no project creation required')
        else: 
            # create project path if path already created but no list_key
            client.secrets.kv.v2.create_or_update_secret(
                path=kwargs.get('project_path'),
                secret=dict(project_id=kwargs.get('l3_asset').get('repo_id')),
                mount_point='tmobile'
            )
            print('\t\tProject Path, added!')
    except hvac.exceptions.InvalidPath:
        # when path does not exist
        client.secrets.kv.v2.create_or_update_secret(
            path=kwargs.get('project_path'),
            secret=dict(project_id=kwargs.get('l3_asset').get('repo_id')),
            mount_point='tmobile'
        )
        print('\t\tProject Path, added!')
    except Exception as e:
        print(f'\n{ error }\n' + str(e) + '\n')
        raise
    finally:
        print(f"\t\tPath Name: {kwargs.get('project_path')}")
