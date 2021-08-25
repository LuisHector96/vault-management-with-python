# T-mobile Enterpise Vault onboarding script

## Getting Started
This repository accomplish automation for onboarding process into T-mobile Enterprise Vault for NPE/PRD environments.

`Currently working on a workflow to automate process using GitLab pipelines.`

### Prerequisites
- Python3 installed
- [Python dependencies](dockerfiles/requirements.txt) installed with `python -m pip`
- A valid certificate to communicate with the Vault (NPE/PRD)
- Admin access granted over the Vault (NPE/PRD)

### Installation

1. Clone repository:
   - ```
     git clone https://gitlab.com/tmobile/TEQ-AP-SM/vault-ent/templates/tev-onboard.git

     cd tev-onboard
     ```

1. Install Python3 in your machine:
   - For MacOS using `Homebrew`:
      - ```
        brew install python
        ```
   - For Linux machine `Ubuntu 20.04`:
      - ```
        sudo apt-get update && apt-get upgrade -y
        sudo apt-get install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libsqlite3-dev libreadline-dev libffi-dev wget libbz2-dev -y
        wget https://www.python.org/ftp/python/3.x.x/Python-3.x.x.tgz
        tar -xf Python-3.x.x.tgz
        cd Python-3.x.x
        ./configure --enable-optimizations
        make -j 8
        make altinstall
        python3.x --version
        ```
1. (optional) Create python virtual environment:
    - ```
      python3.x -m venv <venv_name>
      ```
    - Activate venv:
      - ```
        source <venv_name>/bin/activate
        ```
    - Log out:
      - ```
        deactivate
        ```

1. Install Python dependencies using `requirements.txt` file:
    - ```
      python -m pip install --no-cache-dir -r requirements.txt
      ```

### Usage

(Running locally)
1. Create a `onboard_data.json` file
   - <u>onboard_data.json</u>
     ```
     {
       "onboarding": {
         "<L2_asset>-<L2_apmid>": {
           "L2_APMID": "<L2_ampid>"
         }
       }
     }
     ```
1. Make sure the follow variables are set:
   - ```
     export VAULT_ADDR=https://vault-dev.npe-services.t-mobile.com/
     export VAULT_TOKEN=<vault_token>
     export REONBOARD=false # set to true when re-onboarding needed
     export namespace='tmobile/TEQ-AP-SM' # for Vault onboarding only
     ```
1. To proceed with onboarding process, execute:
   - ```
     python onboarding_main.py <NPE/PRD>
     ```

### Example

1. <u>onboard_data.json</u>
    ```
    {
      "onboarding": {
        "teq-enterprise-vault-ui-apm0201187": {
          "L2_APMID": "APM0201187"
        }
      }
    }
    ```

1. Export variables:
    ````
    export VAULT_ADDR=https://vault-dev.npe-services.t-mobile.com/
    export VAULT_TOKEN=<vault_token>
    export REONBOARD=true # set to true when re-onboarding needed
    export namespace='tmobile/TEQ-AP-SM' # for Vault onboarding only
    ```
1. Run:
    ```
    python onboarding_main.py NPE
    ```

1. Output:

    ```
    You are Authenticated

    Vault Initialized: True
    Vault Sealed: False

    - LDAP validation for AD groups -
    AD group was found!
    REONBOARD variable is set to True, proceeding with reonboarding...

    RUNNING ONBOARDING REQUEST FOR APM0201187 L2 ASSET

      SHARED PATH CREATION:
      Path already exist, no shared/ path to be created
      Path Name: APM0201187/shared/README

      RELIC POLICIES CREATION:
      Relic Policy, added!
      relic-APM0201187

      L2 POLICIES CREATION:
      L2 Admin Policy, added!
      tev-apm0201187-shared-adm
      L2 Read/Write Policy, added!
      tev-apm0201187-shared-rw
      L2 Read Only Policy, added!
      tev-apm0201187-shared-ro

    REQUEST COMPLETED!


      RUNNING ONBOARDING REQUEST FOR APM0201207 L3 ASSET

        PATH CREATION:
        Path already exist, no project creation required
        Path Name: APM0201187/APM0201207/README

        POLICIES CREATION:
        Admin Policy, added!
        tev-apm0201207-adm
        Read/Write Policy, added!
        tev-apm0201207-rw
        Read Only Policy, added!
        tev-apm0201207-ro

        JWT ROLE CREATION:
        JWT Auth Role [NPE], added!

        Role Data:
        role_name:19397766
        bound_claims:{'project_id': '19397766'}
        token_policies:['tev-apm0201207-ro', 'tev-apm0201187-shared-ro', 'relic-APM0201187', 'gitlab-global-ro']

      REQUEST COMPLETED!


      RUNNING ONBOARDING REQUEST FOR DU0245365 L3 ASSET

        PATH CREATION:
        Path already exist, no project creation required
        Path Name: APM0201187/DU0245365/README

        POLICIES CREATION:
        Admin Policy, added!
        tev-du0245365-adm
        Read/Write Policy, added!
        tev-du0245365-rw
        Read Only Policy, added!
        tev-du0245365-ro

        JWT ROLE CREATION:
        JWT Auth Role [NPE], added!

        Role Data:
        role_name:24371932
        bound_claims:{'project_id': '24371932'}
        token_policies:['tev-du0245365-ro', 'tev-apm0201187-shared-ro', 'relic-APM0201187', 'gitlab-global-ro']

      REQUEST COMPLETED!


    EXTERNAL GROUPS:

      Admin oidc external group added!
      oidc_npe_apm0201187_adm
      policies: []

      Admin okt external group added!
      okt_npe_apm0201187_adm
      policies: []

      Admin aad external group added!
      aad_npe_apm0201187_adm
      policies: []

      Read/Write oidc external group added!
      oidc_npe_apm0201187_rw
      policies: []

      Read/Write okt external group added!
      okt_npe_apm0201187_rw
      policies: []

      Read/Write aad external group added!
      aad_npe_apm0201187_rw
      policies: []

      Read Only oidc external group added!
      oidc_npe_apm0201187_ro
      policies: []

      Read Only okt external group added!
      okt_npe_apm0201187_ro
      policies: []

      Read Only aad external group added!
      aad_npe_apm0201187_ro
      policies: []

    INTERNAL GROUPS:

    Admin internal group added!
    tev_APM0201187_adm
    policies: ['tev-apm0201187-shared-adm', 'relic-APM0201187', 'tev-apm0201207-adm', 'tev-du0245365-adm']
    Ext Group Members:
    ['okt_npe_apm0201187_adm', 'oidc_npe_apm0201187_adm', 'aad_npe_apm0201187_adm']

    Read/Write internal group added!
    tev_APM0201187_rw
    policies: ['tev-apm0201187-shared-rw', 'relic-APM0201187', 'tev-apm0201207-rw', 'tev-du0245365-rw']
    Ext Group Members:
    ['okt_npe_apm0201187_rw', 'oidc_npe_apm0201187_rw', 'aad_npe_apm0201187_rw']

    Read Only internal group added!
    tev_APM0201187_ro
    policies: ['tev-apm0201187-shared-ro', 'relic-APM0201187', 'tev-apm0201207-ro', 'tev-du0245365-ro']
    Ext Group Members:
    ['okt_npe_apm0201187_ro', 'aad_npe_apm0201187_ro', 'oidc_npe_apm0201187_ro']


## Contact

- Slack: [#Vault-support](https://t-mo.slack.com/archives/CV0BGHY0Y)

- Email: [TEQAPSM_Vault_Support@T-Mobile.com](mailto:TEQAPSM_Vault_Support@T-Mobile.com)
