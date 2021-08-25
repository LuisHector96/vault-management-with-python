
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
from jinja2 import Template

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Limits traceback messaging, comment for further issue details 
# sys.tracebacklimit = 0

error="->THERE'S AN ERROR Message:<-"

def func_unified_email_templating(**kwargs):

    subject =kwargs.get('email_subject').replace('{{ L2_APM_ID }}', kwargs.get('L2_APMID')).replace('{{ L2_Deployable_Unit_Name }}', kwargs.get('l2_asset_name')).replace('{{ ENV }}', kwargs.get('environment'))
    print(f"\nReceiver: {kwargs.get('l2_owner')}")
    print(f"RELIC Subject: {subject}" )
    try:    
       
        smtp_server = "mailsrv.unix.gsm1900.org"
        port = 25

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = kwargs.get('sender') # Service Account
        message["To"] = kwargs.get('l2_owner') # L2 application owner
        # message["Bcc"] = None  # Recommended for mass emails
        message["Cc"] = 'TEQAPSM_Vault_Support@T-Mobile.com'

        with open(currentdir + '/' + kwargs.get('email_template'), 'r') as email:
            content =email.read()
            t =Template(content)
            html =t.render(ENV=kwargs.get('environment'), L2_Deployable_Unit_Name=kwargs.get('l2_asset_name'), L2_APM_ID=kwargs.get('L2_APMID'), L3_list=kwargs.get('l3_asset_list'),
            tev_env_L2_APMDU_ID_adm=kwargs.get('ad_group_adm'), tev_env_L2_APMDU_ID_rw=kwargs.get('ad_group_rw'), tev_env_L2_APMDU_ID_ro=kwargs.get('ad_group_ro'))
            body =MIMEText(html, "html")
            message.attach(body)
        

        # create rendered file for testing
        with open(f"rendered_{kwargs.get('l2_asset_name')}.html", 'w') as email:
            email.write(html)
            
        
        # Create secure connection with server and send email
        context = ssl.create_default_context()

        # Login to server and send email
        server = smtplib.SMTP(smtp_server,port)
        server.ehlo() # Can be omitted
        if kwargs.get('sending_status'):
            server.sendmail(kwargs.get('sender'), kwargs.get('l2_owner'), message.as_string())
        server.quit()

    except Exception as e:

        print('\nNot able to create email template')
        print(f'\n{ error }\n' + str(e) + '\n')
        raise
