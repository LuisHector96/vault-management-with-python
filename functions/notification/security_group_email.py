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

error = "->THERE'S AN ERROR Message:<-"


def func_security_group_request(**kwargs):

    subject = kwargs.get("email_subject").replace(
        "<group_name>", kwargs.get("group_name")
    )
    print(f"\nReceiver: {kwargs.get('receiver')}")
    print(f"{kwargs.get('role')} SG group request Subject: {subject}")
    try:

        smtp_server = "mailsrv.unix.gsm1900.org"
        port = 25

        message = MIMEMultipart()
        message["Subject"] = subject
        message["From"] = kwargs.get("sender")
        message["To"] = kwargs.get("receiver")
        # message["Bcc"] = None  # Recommended for mass emails
        message["Cc"] = "TEQAPSM_Vault_Support@T-Mobile.com"

        with open(currentdir + "/" + kwargs.get("email_template"), "r") as email:
            content = email.read()
            t = Template(content)
            html = t.render(
                l2_owner=kwargs.get("l2_owner_ntid"),
                env=kwargs.get("environment"),
                group_name=kwargs.get("group_name"),
                L2_CSDMID=kwargs.get("L2_APMID"),
                role=kwargs.get("role"),
                L2_application_name=kwargs.get("l2_asset_name"),
            )
            body = MIMEText(html, "html")
            message.attach(body)

        # create rendered file for testing
        with open(f"request_{kwargs.get('group_name')}.html", "w") as email:
            email.write(html)

        # Create secure connection with server and send email
        context = ssl.create_default_context()

        # Login to server and send email
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted

        if kwargs.get("sending_status"):
            server.sendmail(
                kwargs.get("sender"), kwargs.get("receiver"), message.as_string()
            )
        server.quit()

    except Exception as e:

        print("\nNot able to create Request for Security Group")
        print(f"\n{ error }\n" + str(e) + "\n")
        raise


def func_sg_requests_creation(**kwargs):

    d_values = {**kwargs, "group_name": kwargs.get("ad_group_adm"), "role": "Admin"}
    func_security_group_request(**d_values)

    d_values = {**kwargs, "group_name": kwargs.get("ad_group_rw"), "role": "Read/Write"}
    func_security_group_request(**d_values)

    d_values = {**kwargs, "group_name": kwargs.get("ad_group_ro"), "role": "Read Only"}
    func_security_group_request(**d_values)
