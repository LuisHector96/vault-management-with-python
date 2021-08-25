FROM python:3

WORKDIR /usr/src/app

ENV VAULT_VERSION="1.7.3"

# Quick Update and upgrade
RUN apt update && apt upgrade -y

# Add Hashicorp Vault
RUN curl -sO https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip
RUN unzip vault_${VAULT_VERSION}_linux_amd64.zip
RUN mv vault /usr/local/bin/
RUN vault -autocomplete-install 
#&& complete -C /usr/local/bin/vault vault

# Install job dependencies
RUN apt-get update && apt-get install jq -y

# Install python dependencies
COPY dockerfiles/requirements.txt ./
RUN apt-get install build-essential python3-dev python2.7-dev \
    libldap2-dev libsasl2-dev -y
RUN pip install --no-cache-dir -r requirements.txt

# Install cert for Vault connectivity
COPY certificate.pem ./
COPY add_cert.py ./
RUN python add_cert.py

RUN python --version
RUN vault version

CMD ["python", "Automation_Onboarding.py"]
