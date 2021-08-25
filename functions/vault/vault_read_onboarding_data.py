
import hvac
import json
import sys
import os

# Limits traceback messaging, comment for further issue details 
# sys.tracebacklimit = 0

error="->THERE'S AN ERROR Message:<-"

def func_read_onboard_data(**kwargs):
    """ function to read onboard_data.json file and validates json structure """
    try: 
        with open(kwargs.get('file_name'), 'r') as onboard_data_json_file:
            data_onboarding =json.loads(onboard_data_json_file.read())
            return data_onboarding
    except FileNotFoundError:
        data_onboarding =json.loads(os.environ['ONBOARDING'])
        return data_onboarding
    except Exception as e:
        print(f'\n{ error }\n' + str(e) + '\n')
        raise
