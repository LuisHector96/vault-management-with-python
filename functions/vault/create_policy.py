import hvac
import os
import sys

# Limits traceback messaging, comment for further issue details
# sys.tracebacklimit = 0

error = "->THERE'S AN ERROR Message:<-"


def func_create_policy(client, **kwargs):

    try:
        # create policy
        policy_response = client.sys.create_or_update_policy(
            name=kwargs.get(
                "policy_name"
            ),  # [shared] tev-L3APMID-shared-ROLE, [relic] relic-L2APMID, [L3] tev-L3APMID-ROLE
            policy=kwargs.get("policy"),
        )
        print(f"\t\t{kwargs.get('role')} Policy, added!")
        print(f"\t\t{kwargs.get('policy_name')}")
    except Exception as e:
        print(f"\n{ error }\n" + str(e) + "\n")
        raise


# ----------------
# Execution Time
# ----------------
def func_policy_roles(client, **kwargs):

    return_data = dict()
    # prefix for all policies, internal group
    prefix = kwargs.get("prefix")

    # POLICIES
    print("\n\t\tPOLICIES CREATION:")
    return_data[
        "adm_policy_name"
    ] = f"{kwargs.get('prefix')}-{kwargs.get('L3_APMID').lower()}-adm"
    return_data["adm_policy"] = kwargs.get("admin_policy").replace(
        "GROUP_PATH", kwargs.get("project_path")
    )

    return_data[
        "rw_policy_name"
    ] = f"{kwargs.get('prefix')}-{kwargs.get('L3_APMID').lower()}-rw"
    return_data["rw_policy"] = kwargs.get("read_write_policy").replace(
        "GROUP_PATH", kwargs.get("project_path")
    )

    return_data[
        "ro_policy_name"
    ] = f"{kwargs.get('prefix')}-{kwargs.get('L3_APMID').lower()}-ro"
    return_data["ro_policy"] = kwargs.get("read_only_policy").replace(
        "GROUP_PATH", kwargs.get("project_path")
    )

    return_data[
        "mr_ro_policy_name"
    ] = f"{kwargs.get('prefix')}-{kwargs.get('L2_APMID').lower()}-{kwargs.get('L3_APMID').lower()}-ro"
    return_data["mr_ro_policy"] = (
        kwargs.get("read_only_policy").replace("GROUP_PATH", kwargs.get("project_path"))
        + "\n"
        + kwargs.get("l2_shared_ro")
        + "\n"
        + kwargs.get("relic")
    )

    return_data[
        "adm_pcf_policy_name"
    ] = f"pcf-{kwargs.get('L3_APMID').lower()}-role-adm"
    return_data["adm_pcf_policy"] = (
        kwargs.get("policy_pcf_admin")
        .replace("POLICY_NAME", return_data["mr_ro_policy_name"])
        .replace("L3_CSDMID", kwargs.get("L3_APMID").lower())
    )

    # create
    d_values = {
        "policy_name": return_data.get("adm_policy_name"),
        "policy": return_data.get("adm_policy"),
        "role": "Admin",
    }
    func_create_policy(client, **d_values)
    d_values = {
        "policy_name": return_data.get("rw_policy_name"),
        "policy": return_data.get("rw_policy"),
        "role": "Read/Write",
    }
    func_create_policy(client, **d_values)
    d_values = {
        "policy_name": return_data.get("ro_policy_name"),
        "policy": return_data.get("ro_policy"),
        "role": "Read Only",
    }
    func_create_policy(client, **d_values)
    d_values = {
        "policy_name": return_data.get("mr_ro_policy_name"),
        "policy": return_data.get("mr_ro_policy"),
        "role": "MR read only",
    }
    func_create_policy(client, **d_values)
    d_values = {
        "policy_name": return_data.get("adm_pcf_policy_name"),
        "policy": return_data.get("adm_pcf_policy"),
        "role": "L3 PCF Role Admin",
    }
    func_create_policy(client, **d_values)

    return return_data
