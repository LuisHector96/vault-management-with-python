import hvac
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir)
import json
from snow_api_call import *

# Limits traceback messaging, comment for further issue details
# sys.tracebacklimit = 0

error = "->THERE'S AN ERROR Message:<-"


def func_snow_request_creation(client, **kwargs):

    return_data = dict()

    keys = client.secrets.kv.v2.read_secret_version(
        mount_point="admin",
        path="apigee/201187-TEQ Enterprise Vault-DEVAPP",
    )
    strPrivate = keys.get("data").get("data").get("pop-private-key-pkcs8.pem")
    strPublic = keys.get("data").get("data").get("pop-public-key.pem")
    clientID = keys.get("data").get("data").get("client_id")
    clientScr = keys.get("data").get("data").get("secret_key")

    ad_request = func_snow_response(
        kwargs.get("url_snow"), strPrivate, strPublic, clientID, clientScr
    )

    try:
        ad_request = ad_request.json()
        if ad_request.get("success"):
            return_data["manual_ad_groups_creation"] = False
            print(
                "\nActive Directory Group creation successful!"
                + "\nRequest ID: "
                + ad_request.get("message").get("result").get("request_number")
            )
        else:
            return_data["manual_ad_groups_creation"] = True
            print(
                "\nWARNING"
                + "\nActive Directory Group creation was NOT completed!"
                + "\nOutput:\n"
                + str(ad_request)
            )
    except json.decoder.JSONDecodeError:
        print(
            "\nWARNING\nActive Directory Group creation was NOT completed!\nOutput:\n"
            + str(ad_request)
        )
    except:
        print(f"\n{ error }\n")
        raise

    return return_data
