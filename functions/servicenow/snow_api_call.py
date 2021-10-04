try:
    from snow_access_token import *
    import requests
    import json
except Exception as e:
    print(str(e))


def func_snow_response(url, strPrivate, strPublic, clientID, clientScr):

    # access token has validity of 1 hour
    accessTok = access_token(strPrivate, strPublic, clientID, clientScr)

    popTok = create_pop(url, strPrivate, strPublic)

    # access api endpoints using python request lib
    headers = {
        "X-Authorization": popTok,
        "Authorization": "Bearer " + accessTok,
    }

    response = requests.request("GET", url, headers=headers)
    # print(response.text)
    return response


def main():

    import hvac
    import os

    # data to connect to the vault
    vault_addr = os.environ["VAULT_ADDR"]
    vault_token = os.environ["VAULT_TOKEN"]

    # ---------------------------
    # Vault Client - VAULT_ADDR
    # ---------------------------
    # NOTE: needs variables.py to work
    client = hvac.Client(
        url=vault_addr,
        token=vault_token,
        # verify=False, # In case you want to run without validating certs
    )

    keys = client.secrets.kv.v2.read_secret_version(
        mount_point="admin",
        path="apigee/201187-TEQ Enterprise Vault-DEVAPP",
    )
    strPrivate = keys.get("data").get("data").get("pop-private-key-pkcs8.pem")
    strPublic = keys.get("data").get("data").get("pop-public-key.pem")
    clientID = keys.get("data").get("data").get("client_id_prd")
    clientScr = keys.get("data").get("data").get("secret_key_prd")

    # https://tmobilea-sb02.apigee.net/api/asset-portfolio/v1/asset-ad-group/{csdm}
    url = "https://tmobilea-sb02.apigee.net/api/asset-portfolio/v1/asset-ad-group/APM0225334?environment=development"
    ad_request = func_canvas_response(url, strPrivate, strPublic, clientID, clientScr)
    ad_request = ad_request.json()
    try:
        if ad_request.get("success"):
            print(ad_request)
        else:
            print("failed, but proceed to slack")
    except:
        raise


if __name__ == "__main__":
    main()
