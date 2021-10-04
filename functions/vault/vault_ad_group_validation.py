import hvac
import ldap
import os, sys

# Limits traceback messaging, comment for further issue details
# sys.tracebacklimit = 0

error = "->THERE'S AN ERROR Message:<-"


def func_ldap_validation(**kwargs):
    """function to validate AD group exist in Active Directory"""

    try:
        ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        l = ldap.initialize(kwargs.get("ldap_addr"))
        l.set_option(ldap.OPT_REFERRALS, 0)
        l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        l.set_option(ldap.OPT_X_TLS, ldap.OPT_X_TLS_DEMAND)
        l.set_option(ldap.OPT_X_TLS_DEMAND, True)
        l.set_option(ldap.OPT_DEBUG_LEVEL, 255)
        l.simple_bind_s(kwargs.get("ldap_user"), kwargs.get("ldap_password"))
        search_for = l.search_s(
            "OU=SECURE,OU=ServiceNow,OU=Groups,OU=User Accounts,DC=gsm1900,DC=org",
            ldap.SCOPE_SUBTREE,
            filterstr=f"CN={kwargs.get('ad_group')}*",
        )
        group = search_for[0][1].get("cn")
        return True
    except ldap.NO_SUCH_OBJECT:
        # assert(False), 'no group found'
        return False
    except IndexError:
        return False
    except Exception as e:
        print("Error Message:\n" + str(e))
        raise


# ----------------
# Execution Time
# ----------------


def func_ad_group_validation(client, **kwargs):

    return_data = dict()

    print("\n- LDAP validation for AD groups -")
    ldap_validation_response = func_ldap_validation(**kwargs)
    if ldap_validation_response:
        print("AD group was found!")
        return_data["ad_group_created"] = True
    else:
        print("No AD group found, proceeding with creation request...\n")
        return_data["ad_group_created"] = False
    return return_data
