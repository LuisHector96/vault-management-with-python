import hvac
import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(currentdir)
from canvas_api_call import *

# Limits traceback messaging, comment for further issue details
# sys.tracebacklimit = 0

error = "->THERE'S AN ERROR Message:<-"


def func_l2_asset_validation(**kwargs):
    """function to gather all necessary information for onboarding (L3 APMIDs with repo id associated, L2 asset data)"""

    return_data = dict()

    url_l2_data = f"{kwargs.get('url_l2_asset')}/{kwargs.get('L2_APMID')}"

    try:

        canvas_l2_data = func_canvas_response(
            url_l2_data,
            kwargs.get("strPrivate"),
            kwargs.get("strPublic"),
            kwargs.get("clientID"),
            kwargs.get("clientScr"),
        )

        # validates L2 is an L2 apmid
        assert (
            canvas_l2_data.get("subclass") == "Application"
            or canvas_l2_data.get("subclass") == "Platform"
        ), "not an L2 APMID value, please validate"

        # l2 data collection
        return_data["l1_asset"] = canvas_l2_data.get("parentBusinessApplication")
        return_data["l2_owner_ntid"] = canvas_l2_data.get("ownedByNtid")
        return_data["l2_asset_name"] = canvas_l2_data.get("name")
        if canvas_l2_data.get("compliance").get("pci_control") == "Yes":
            return_data["l2_pci_in_scope"] = True
        elif canvas_l2_data.get("compliance").get("pci_control") == "No":
            return_data["l2_pci_in_scope"] = False
        if canvas_l2_data.get("compliance").get("sox_control") == "Yes":
            return_data["l2_sox_in_scope"] = True
        elif canvas_l2_data.get("compliance").get("sox_control") == "No":
            return_data["l2_sox_in_scope"] = False
        return_data["l3_asset_list"] = canvas_l2_data.get("childBusinessApplications")
        return_data["l3_apmid_list"] = [
            l3_asset.get("id") for l3_asset in return_data.get("l3_asset_list")
        ]

        # l2 application owner data
        url_l2_owner_data = (
            f"{kwargs.get('url_l2_owner')}={return_data.get('l2_owner_ntid')}"
        )
        canvas_l2_owner_data = func_canvas_response(
            url_l2_owner_data,
            kwargs.get("strPrivate"),
            kwargs.get("strPublic"),
            kwargs.get("clientID"),
            kwargs.get("clientScr"),
        )

        # owner data collection
        return_data["l2_owner_email"] = next(
            canvas_l2_owner_data[index].get("email")
            for index in range(len(canvas_l2_owner_data))
            if canvas_l2_owner_data[index].get("ntid")
            == return_data.get("l2_owner_ntid")
        )
        return_data["l3_with_repo_list"] = []
        return_data["l3_based_in_repo_list"] = dict()

        # Get L3 APMIDs list with repo id associated
        for L3_APMID in return_data.get("l3_apmid_list"):

            url_l3_repo_data = f"{kwargs.get('url_l3_asset')}={L3_APMID}"
            canvas_l3_repo_data = func_canvas_response(
                url_l3_repo_data,
                kwargs.get("strPrivate"),
                kwargs.get("strPublic"),
                kwargs.get("clientID"),
                kwargs.get("clientScr"),
            )

            if canvas_l3_repo_data.get("reposFound"):
                return_data["l3_with_repo_list"].append(
                    {
                        "id": L3_APMID,
                        "repo_id": canvas_l3_repo_data.get("repos")[0].get("repoId"),
                    }
                )

                try:
                    return_data["l3_based_in_repo_list"][
                        f"{canvas_l3_repo_data.get('repos')[0].get('repoId')}"
                    ].append(L3_APMID)
                except KeyError:
                    return_data["l3_based_in_repo_list"][
                        f"{canvas_l3_repo_data.get('repos')[0].get('repoId')}"
                    ] = [L3_APMID]

        return return_data

    except AssertionError:
        raise
    except Exception as e:
        print(f"\n{ error }\n" + str(e) + "\n")
        raise


# ----------------
# Execution Time
# ----------------
def func_canvas(client, **kwargs):

    resp = client.secrets.kv.v2.read_secret_version(
        mount_point="admin",
        path="apigee/201187-TEQ Enterprise Vault-DEVAPP",
    )

    strPrivate = resp.get("data").get("data").get("pop-private-key-pkcs8.pem")
    strPublic = resp.get("data").get("data").get("pop-public-key.pem")
    clientID = resp.get("data").get("data").get("client_id_prd")
    clientScr = resp.get("data").get("data").get("secret_key_prd")

    d_values = {
        **kwargs,
        "strPrivate": strPrivate,
        "strPublic": strPublic,
        "clientID": clientID,
        "clientScr": clientScr,
    }
    canvas_data = func_l2_asset_validation(**d_values)
    return canvas_data
