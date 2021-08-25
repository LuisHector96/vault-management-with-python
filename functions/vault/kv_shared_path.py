
import hvac
import os
import sys

# Limits traceback messaging, comment for further issue details 
# sys.tracebacklimit = 0

error="->THERE'S AN ERROR Message:<-"


def func_l2_shared_path(client, **kwargs):
    """ function to create shared path where secrets can be accessed all over the deployable units"""

    print('\n\tSHARED PATH CREATION:')
    # check if project path already created or not
    try:
        # list all keypaths in the specific path
        list_response = client.secrets.kv.v2.list_secrets(
            path=kwargs.get('L2_APMID'),
            mount_point='tmobile'
        )

        # validate shared path exist
        if kwargs.get('shared_secret') in list_response['data']['keys']:
            print('\tPath already exist, no shared/ path to be created')
        else: 
            # create shared space if path already created but no shared path
            client.secrets.kv.v2.create_or_update_secret(
                path=kwargs.get('shared_path'),
                secret=dict(README=kwargs.get('readme')),
                mount_point='tmobile'
            )
            print('\tshared/ path added!')
    except hvac.exceptions.InvalidPath:
        # when path does not exist
        client.secrets.kv.v2.create_or_update_secret(
            path=kwargs.get('shared_path'),
            secret=dict(README=kwargs.get('readme')),
            mount_point='tmobile'
        )
        print('\tshared/ path added!')
    except Exception as e:
        print(f'\n{ error }\n' + str(e) + '\n')
        raise
    finally:
        print(f"\tPath Name: {kwargs.get('shared_path')}")
