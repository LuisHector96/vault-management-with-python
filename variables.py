import sys
import os

#-----------------------
# Static Global Variables
#-----------------------

# prefix for policies and groups
prefix='tev'

# output log file name
stdout_file='std_output.log'

# onboard data file name to look for
onboard_data_file='onboard_data.json'

# readme message for README kv paths
readme_message="Folders do not exist unless at least one secret is inside. This README is placed to ensure the folder appears in the Vault UI."

# LDAP validation endpoint
ldap_addr='ldaps://secldapwest.gsm1900.org:636'

# Canvas Endpoints
# url for canvas api email l2 owner
url_l2_owner ='https://core.saas.api.t-mobile.com/api/asset-portfolio/v2/employee-details?ntid'
# url for canvas api L2 asset
url_l2_asset ='https://core.saas.api.t-mobile.com/api/asset-portfolio/v2/business-application'
# url for canvas api L3 asset
url_l3_asset ='https://core.saas.api.t-mobile.com/api/asset-portfolio/v1/associated-repos?csdmNumber'
# url for canvas api gitlab id
url_gitlab_id ='https://core.saas.api.t-mobile.com/api/asset-portfolio/v1/associated-assets?CI_PROJECT_ID'

# Emailing
# service accounts
npe_relic_sender ='SVC_DEV_relic_onbrd@T-Mobile.com'
npe_vault_sender ='SVC_DEV_vault_onbrd@T-Mobile.com'
prd_relic_sender ='SVC_PRD_relic_onbrd@T-Mobile.com'
prd_vault_sender ='SVC_PRD_vault_onbrd@T-Mobile.com'
# subjects
relic_email_subject ='[RELIC Onboarding] {{ L2_APM_ID }} - {{ L2_Deployable_Unit_Name }} has been onboarded to RELIC {{ ENV }} platform'
vault_email_subject ='[Vault Onboarding] {{ L2_APM_ID }} - {{ L2_Deployable_Unit_Name }} has been onboarded to Vault {{ ENV }}'
sg_email_request_subject ='[Request to create active directory security group with a secure ACL] [GroupName:<group_name>]'
# templates
vault_template ='vault_only_onboarding.html'
unified_template ='unified_onboarding.html'
sg_email_file ='sg_request.html'

#-----------------------------
# Input Global Variables
#-----------------------------

# export commands
# export VAULT_ADDR=https://vault-dev.npe-services.t-mobile.com/
# export VAULT_TOKEN=$(cat ~/.vault-token)
# export REONBOARD=true
# export PARENT_PROJECT_NAMESPACE='tmobile/TEQ-AP-SM'
# export email_notification=true
# export sg_email=true

# argument to specify which vault environment want to hit (PRD/NPE)
environment=sys.argv[1]

# data to connect to the vault
vault_addr=os.environ['VAULT_ADDR']
vault_token=os.environ['VAULT_TOKEN']

# manage reonboarding process
REONBOARD=True if (os.environ['REONBOARD'].title() == 'True') else False

# select for which onboarding to run: 
# export namespace='tmobile/TEQ-AP-SM' (for vault onboarding)
# Everything else will be taken as RELIC onboarding
namespace =os.environ['PARENT_PROJECT_NAMESPACE']
