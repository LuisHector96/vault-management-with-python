import hvac
import os
import sys
import requests

# Limits traceback messaging, comment for further issue details
# sys.tracebacklimit = 0

error = "->THERE'S AN ERROR Message:<-"


def func_create_jwt_role(client, **kwargs):
    """function to create jwt role for cdp pipelines"""

    if kwargs.get("environment") == "PRD":
        bound_claims_data = dict(project_id=kwargs.get("repo_id"), ref_protected="true")
    else:
        bound_claims_data = dict(project_id=kwargs.get("repo_id"))

    print("\n\t\tJWT ROLE CREATION:")

    try:
        allowed_redirect_uris = None
        client.auth.jwt.create_role(
            name=kwargs.get("repo_id"),
            role_type="jwt",
            allowed_redirect_uris=allowed_redirect_uris,
            token_policies=kwargs.get("read_policies"),
            token_explicit_max_ttl="1h",
            user_claim="project_id",
            bound_claims_type="glob",
            bound_claims=bound_claims_data,
            claim_mappings=dict(
                environment_protected="gitlab_env_protected",
                environment="gitlab_env",
                iss="gitlab_issuer_domain",
                job_id="gitlab_job_id",
                jti="gitlab_json_token_id",
                namespace_id="gitlab_namespace_id",
                namespace_path="gitlab_namespace_path",
                pipeline_id="gitlab_pipeline_id",
                project_id="gitlab_project_id",
                project_path="gitlab_project_path",
                ref_protected="gitlab_ref_protected",
                ref_type="gitlab_ref_type",
                ref="gitlab_ref",
                sub="gitlab_json_token_subject",
                user_email="gitlab_caller_email",
                user_id="gitlab_caller_id",
            ),
            path="cdp",
        )
        # Read Role
        response = client.auth.jwt.read_role(name=kwargs.get("repo_id"), path="cdp")
        print("\t\tJWT Auth Role [NPE], added!\n")
        print(
            f"\t\tRole Data:\n\t\trole_name:{kwargs.get('repo_id')}\n\t\tbound_claims:{response.get('data').get('bound_claims')}\n\t\ttoken_policies:{response.get('data').get('token_policies')}"
        )

    except Exception as e:
        print(f"\n{ error }\n" + str(e) + "\n")
        raise


def func_global_entity(client, **kwargs):

    try:
        entity_response = client.secrets.identity.lookup_entity(
            name=kwargs.get("cdp_entity"),
        )

        entity_id = entity_response.get("data").get("id")

        create_response = client.secrets.identity.create_or_update_entity_alias(
            name=kwargs.get("repo_id"),
            canonical_id=entity_id,
            mount_accessor=kwargs.get("accessor"),
        )
    except AttributeError:
        url = kwargs.get("vault_addr") + "/v1/identity/lookup/entity"
        headers = {
            "X-Vault-Token": kwargs.get("vault_token"),
            "X-Vault-Namespace": "cde/",
        }
        data = {"name": kwargs.get("cdp_entity")}
        r = requests.post(url, headers=headers, data=data, verify=False)
        print(r)
        r = r.json()
        print(r)
        entity_id = r.get("data").get("id")
        print(entity_id)

        create_response = client.secrets.identity.create_or_update_entity_alias(
            name=kwargs.get("repo_id"),
            canonical_id=entity_id,
            mount_accessor=kwargs.get("accessor"),
        )

    except Exception as e:
        print(f"\n{ error }\n" + str(e) + "\n")
        raise


# ----------------
# Execution Time
# ----------------
def func_jwt_role(client, **kwargs):

    func_create_jwt_role(client, **kwargs)
    func_global_entity(client, **kwargs)
