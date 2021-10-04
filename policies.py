# --------------------
# Policies Definition
# --------------------

# Using GROUP_PATH & L2_APMID as the identifier for replacement with actual value
Admin_policy = """
path "tmobile/*"{
capabilities = ["list"]
}
# Deployable Unit
path "tmobile/data/GROUP_PATH"{
capabilities = ["create", "read", "update", "delete", "list"]
}
path "tmobile/metadata/GROUP_PATH"{
capabilities = ["create", "read", "update", "delete", "list"]
}
path "tmobile/delete/GROUP_PATH" {
capabilities = ["update"]
}
path "tmobile/undelete/GROUP_PATH" {
capabilities = ["update"]
}
path "tmobile/destroy/GROUP_PATH" {
capabilities = ["update"]
}
path "tmobile/data/GROUP_PATH/*"{
capabilities = ["create", "read", "update", "delete", "list"]
}
path "tmobile/metadata/GROUP_PATH/*"{
capabilities = ["create", "read", "update", "delete", "list"]
}
path "tmobile/delete/GROUP_PATH/*" {
capabilities = ["update"]
}
path "tmobile/undelete/GROUP_PATH/*" {
capabilities = ["update"]
}
path "tmobile/destroy/GROUP_PATH/*" {
capabilities = ["update"]
}
"""

Read_Write_policy = """
path "tmobile/*"{
capabilities = ["list"]
}
path "tmobile/data/GROUP_PATH"{
capabilities = ["create", "read", "update", "list"]
}
path "tmobile/metadata/GROUP_PATH"{
capabilities = ["create", "read", "update", "list"]
}
path "tmobile/data/GROUP_PATH/*"{
capabilities = ["create", "read", "update", "list"]
}
path "tmobile/metadata/GROUP_PATH/*"{
capabilities = ["create", "read", "update", "list"]
}
"""

Read_Only_policy = """
path "tmobile/*"{
capabilities = ["list"]
}
path "tmobile/data/GROUP_PATH"{
capabilities = ["read", "list"]
}
path "tmobile/metadata/GROUP_PATH"{
capabilities = ["read", "list"]
}
path "tmobile/data/GROUP_PATH/*"{
capabilities = ["read", "list"]
}
path "tmobile/metadata/GROUP_PATH/*"{
capabilities = ["read", "list"]
}
"""

# Relic policy
Relic_policy = """
# "relic-kv/data/onboarding/+/+/APM0000000/*"
# first [+] for environment
# second [+/+] for L1 asset

path "relic-kv/data/onboarding/+/+/L2_APMID/*" {
  capabilities = ["read"]
}
path "relic-kv/metadata/onboarding/*" {
  capabilities = ["list"]
}
path "relic-kv/metadata/onboarding" {
  capabilities = ["list"]
}
path "relic-kv/metadata" {
  capabilities = ["list"]
}
"""

# L2 level policies
L2_Policy_adm = """
path "tmobile/data/L2_APMID/shared/*"{
capabilities = ["create", "read", "update", "delete", "list"]
}
path "tmobile/metadata/L2_APMID/shared/*"{
capabilities = ["create", "read", "update", "delete", "list"]
}
path "tmobile/delete/L2_APMID/shared/*" {
capabilities = ["update"]
}
path "tmobile/undelete/L2_APMID/shared/*" {
capabilities = ["update"]
}
path "tmobile/destroy/L2_APMID/shared/*" {
capabilities = ["update"]
}
"""

L2_Policy_rw = """
path "tmobile/data/L2_APMID/shared/*"{
capabilities = ["create", "read", "update", "delete", "list"]
}
path "tmobile/metadata/L2_APMID/shared/*"{
capabilities = ["create", "read", "update", "list"]
}
"""

L2_Policy_ro = """
path "tmobile/data/L2_APMID/shared/*"{
capabilities = ["read", "list"]
}
path "tmobile/metadata/L2_APMID/shared/*"{
capabilities = ["read", "list"]
}
"""

L3_Policy_pcf_adm = """
# PCF Privileged Role Management Delegation Policy
# Name: pcf-L3_CSDMID-role-adm

path "auth/pcf/+/roles" {
  capabilities = ["list"]
}

path "auth/pcf/+/roles/*" {
  capabilities = ["read"]
}

path "auth/pcf/+/roles/L3_CSDMID" {
  capabilities = ["create", "read", "update", "delete"]

  allowed_parameters = {
    "token_policies" = [
      "POLICY_NAME",
    ]

    "*" = []
  }

  required_parameters = ["bound_space_ids", "bound_organization_ids"]

  denied_parameters = {
    "token_period" = []
  }
}

"""
