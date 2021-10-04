import hvac
import os, sys

# Limits traceback messaging, comment for further issue details
# sys.tracebacklimit = 0

error = "->THERE'S AN ERROR Message:<-"


## Internal Group ##
def func_create_internal_group(client, **kwargs):
    """function to create internal groups, groups that provides actual permissions over the vault"""

    return_data = dict()

    return_data["int_grp_name"] = kwargs.get("int_grp_name")
    return_data["int_policies"] = kwargs.get("int_policies")
    try:
        # create internal group
        client.secrets.identity.create_or_update_group_by_name(
            name=kwargs.get(
                "int_grp_name"
            ),  #'{}-{}-{}'.format(project_id, project_name, policy_kind),
            group_type="internal",
            policies=kwargs.get("int_policies") + ["default"],
            member_group_ids=",".join(kwargs.get("external_groups")),
            metadata=dict(
                metadata=str(kwargs.get("metadata")),
            ),
        )
        print(f"\n{kwargs.get('message')}")
        print(
            f"{kwargs.get('int_grp_name')}"
        )  #'{}-{}-{}'.format(project_id, project_name, policy_kind))

        read_group = client.secrets.identity.read_group_by_name(
            name=kwargs.get("int_grp_name"),
        )
        print("policies: " + str(read_group.get("data").get("policies")))

        # read members and print
        try:
            groups = read_group["data"]["member_group_ids"]
            return_data["ext_grp_member_ids"] = groups

            group_list = []
            for group in groups:
                read_response = client.secrets.identity.read_group(
                    group_id=group,
                )
                group_name = read_response["data"]["name"]
                group_list.append(group_name)

            print("Ext Group Members:")
            print(group_list)
            return_data["ext_grp_member_names"] = group_list

        except:
            print("no external groups for this internal group")

    except Exception as e:
        print(f"{kwargs.get('int_group_name')} Internal Group was NOT added...")
        print(f"\n{ error }\n" + str(e) + "\n")
        raise

    finally:
        return return_data


# ----------------
# Execution Time
# ----------------
def func_internal_groups(client, **kwargs):

    return_data = dict()
    print("\nINTERNAL GROUPS:")

    metadata = {"L2_APMID": kwargs.get("L2_APMID")}

    # ADMIN
    adm_int_grp_policies = [
        kwargs.get("policies").get("l2_adm_shared"),
        kwargs.get("policies").get("relic"),
    ]
    adm_int_grp_policies.extend(kwargs.get("policies").get("adm"))
    adm_int_grp_policies.extend(kwargs.get("policies").get("pcf"))
    adm_ext_member_ids = [
        value
        for key, value in kwargs.get("external_groups").get("adm_ext_groups").items()
    ]
    adm_int_grp_name = f"{kwargs.get('prefix')}_{kwargs.get('L2_APMID')}_adm"
    d_values = {
        "int_grp_name": adm_int_grp_name,
        "int_policies": adm_int_grp_policies,
        "external_groups": adm_ext_member_ids,
        "message": "Admin internal group added!",
        "metadata": metadata,
    }
    return_data["int_adm_grp"] = func_create_internal_group(client, **d_values)

    # READ/WRITE
    rw_int_grp_policies = [
        kwargs.get("policies").get("l2_rw_shared"),
        kwargs.get("policies").get("relic"),
    ]
    rw_int_grp_policies.extend(kwargs.get("policies").get("rw"))
    rw_ext_member_ids = [
        value
        for key, value in kwargs.get("external_groups").get("rw_ext_groups").items()
    ]
    rw_int_grp_name = f"{kwargs.get('prefix')}_{kwargs.get('L2_APMID')}_rw"
    d_values = {
        "int_grp_name": rw_int_grp_name,
        "int_policies": rw_int_grp_policies,
        "external_groups": rw_ext_member_ids,
        "message": "Read/Write internal group added!",
        "metadata": metadata,
    }
    return_data["int_rw_grp"] = func_create_internal_group(client, **d_values)

    # READ ONLY
    ro_int_grp_policies = [
        kwargs.get("policies").get("l2_ro_shared"),
        kwargs.get("policies").get("relic"),
    ]
    ro_int_grp_policies.extend(kwargs.get("policies").get("ro"))
    ro_ext_member_ids = [
        value
        for key, value in kwargs.get("external_groups").get("ro_ext_groups").items()
    ]
    ro_int_grp_name = f"{kwargs.get('prefix')}_{kwargs.get('L2_APMID')}_ro"
    d_values = {
        "int_grp_name": ro_int_grp_name,
        "int_policies": ro_int_grp_policies,
        "external_groups": ro_ext_member_ids,
        "message": "Read Only internal group added!",
        "metadata": metadata,
    }
    return_data["int_ro_grp"] = func_create_internal_group(client, **d_values)

    return return_data
