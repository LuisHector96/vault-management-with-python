# this module can be imported to create access token which is used for sunsequent API calls as bearer authorization token; or to create pop token for given URL

# some of the installation depency required
# recommend using virtual env so that those dependencies are installed in a controlled manner
# pip install PyJWT
# pip install cryptography
import jwt
import time
import hashlib
import base64
import uuid
import sys
import requests
import json
import os


def create_jwt(dictPara, strPrivate):
    # need to check if private key has been loaded as str obj
    if not strPrivate:
        print("Private key string obj strPrivate has not been loaded, exiting")
        quit()
    lstEHTS = []
    strHeaders = ""
    for strKey in dictPara.keys():
        lstEHTS.append(strKey)
        strHeaders += dictPara[strKey]

    strEHTS = ";".join(lstEHTS)
    dictBody = {}
    dictBody["iat"] = int(time.time())
    dictBody["exp"] = dictBody["iat"] + 120
    dictBody["ehts"] = strEHTS
    strTemp = base64.urlsafe_b64encode(
        hashlib.sha256(str(strHeaders).encode("utf-8")).digest()
    )
    strTemp = strTemp.decode("utf-8")
    dictBody["edts"] = strTemp[:-1]
    dictBody["jti"] = str(uuid.uuid4())
    dictBody["v"] = 1

    strSigned = jwt.encode(dictBody, strPrivate, algorithm="RS256")
    return strSigned


# funcntion to create access token
def access_token(strPrivate, strPublic, clientID, clientScr):
    dictJWTBody = {}
    dictJWTBody["URI"] = "/oauth2/v6/tokens"
    # strSigned would be the pop token generated for the particular URI endpoint we have generated
    strSigned = create_jwt(dictJWTBody, strPrivate)
    # strDecode is the decoded pop token
    strDecode = jwt.decode(strSigned, strPublic, algorithms=["RS256"])
    # now generate the access token
    x_auth_header = strSigned
    auth_header = "Basic " + base64.b64encode(
        (clientID + ":" + clientScr).encode("utf-8")
    ).decode("utf-8")
    url = "https://tmobilea-sb02.apigee.net/oauth2/v6/tokens"
    payload = json.dumps({})
    headers = {
        "X-Authorization": x_auth_header,
        "Authorization": auth_header,
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    accessToken = response.json()["access_token"]

    # print (accessToken)
    return accessToken


# function to create pop token based on a particular url
def create_pop(url, strPrivate, strPublic):
    dictJWTBody = {}
    if "apigee.net" in url:
        uri = url.split("apigee.net", 1)[1]
    elif "t-mobile.com" in url:  # this is for prod url
        uri = url.split("t-mobile.com", 1)[1]
    else:
        uri = url

    dictJWTBody["URI"] = uri
    # strSigned would be the pop token generated for the particular URI endpoint we have generated
    strSigned = create_jwt(dictJWTBody, strPrivate)
    # strDecode is the decoded pop token, good for validation etc.
    strDecode = jwt.decode(strSigned, strPublic, algorithms=["RS256"])
    return strSigned
