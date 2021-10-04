#!/bin/bash

#VAULT_TOKEN=$(curl -s --request POST --data "{\"jwt\":\"${CI_JOB_JWT}\",\"role\":\"${CI_PROJECT_ID}\"}" "${VAULT_ADDR}/v1/auth/cdp/login" | jq -r '.auth.client_token')
#export VAULT_TOKEN
if [[ "${ENV}" == "NPE" ]]; then tevenv="DEV"; else tevenv="${ENV}"; fi
if [[ "${TEST_JOB}" == "true" ]]; then cdp_role="${ROLE}"; else cdp_role="${CI_PROJECT_ID}"; fi
if tevAuth --environment "${tevenv}" --authpath gitlab --authrole "${cdp_role}" -v ; then
  trap "if ! tevRevoke -v; then echo 'revoke error'; fi" EXIT QUIT TERM ABRT INT
else
  exit
fi
echo "PARENT_PROJECT_ID = ${PARENT_PROJECT_ID}"
echo "PARENT_PIPELINE_ID = ${PARENT_PIPELINE_ID}"
echo "PARENT_PROJECT_NAMESPACE = ${PARENT_PROJECT_NAMESPACE}"
echo "L1 = ${L1}"
echo "ENV = ${ENV}"
echo "REONBOARD = ${REONBOARD}"
echo "EMAIL_RESEND = ${EMAIL_RESEND}"
echo "TEST_JOB = ${TEST_JOB}"
echo "ROLE = ${ROLE}"
if [[ ! $PARENT_PROJECT_NAMESPACE =~ ^"tmobile/TEQ-AP-SM" ]];then
    #ARTIFACT_TOKEN=$(curl -s --header "X-Vault-Token:${VAULT_TOKEN}" --request GET "${VAULT_ADDR}/v1/admin/data/vault_onboarding" | jq -r ".data.data.GL_TKN")
    tevGetSecret -v --output-variable ARTIFACT_TOKEN --kvv2path admin/vault_onboarding --field GL_TKN
    export ARTIFACT_TOKEN
    job_id=$(
      curl -s --location --header "PRIVATE-TOKEN:${ARTIFACT_TOKEN}" \
      "https://gitlab.com/api/v4/projects/${PARENT_PROJECT_ID}/pipelines/${PARENT_PIPELINE_ID}/jobs" |
      jq -c '.[] | select( .name | contains("pre-onboard"))' |
      jq .id
    )
    curl -s --location --output artifacts.zip --header "PRIVATE-TOKEN:${ARTIFACT_TOKEN}" \
      "https://gitlab.com/api/v4/projects/${PARENT_PROJECT_ID}/jobs/${job_id}/artifacts"
    unzip artifacts.zip
    ONBOARDING=$(< build.env jq -r '.')
fi
echo "${ONBOARDING}" | jq '.' > onboard_data.json
< onboard_data.json jq -r '.'
if [[ "${TEST_JOB}" == "true" ]]; then
  python tests/test_main.py ${ENV}
else
  ython ./onboarding_main.py ${ENV}
fi
rm onboard_data.json
eval "$(cat .env)"
#webhook_url=$(curl -s --header "X-Vault-Token:${VAULT_TOKEN}" --request GET "${VAULT_ADDR}/v1/admin/data/slack-webhook" | jq -r '.data.data.url')
tevGetSecret -v --output-variable webhook_url --kvv2path admin/slack-webhook --field url
message="<@U01J7V7HA05> <@W0128MW1EE8> <@W013BER7064> <@U01JA7RNV0Q> Pipeline ${CI_JOB_ID} has completed! Please view job artifacts and send emails as required - ${CI_PROJECT_URL}/-/jobs/${CI_JOB_ID}/artifacts/browse"
if [ "${SLACK}" == "true" ]; then slackNotify "${message}" "${webhook_url}"; else echo 'no slack notification sent'; fi
#curl -s --header "X-Vault-Token:${VAULT_TOKEN}" --request POST "${VAULT_ADDR}/v1/auth/token/revoke-self"
#if  echo $?; then echo 'Token revoked!'; else echo 'revokation not executed...'; fi
