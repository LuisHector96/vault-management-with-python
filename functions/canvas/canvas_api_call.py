
try:
    from canvas_access_token import *
    import requests
    import json
except Exception as e:
    print(str(e))



def func_canvas_response(url, strPrivate, strPublic, clientID, clientScr):

    # access token has validity of 1 hour
    accessTok = access_token(strPrivate, strPublic, clientID, clientScr)

    popTok = create_pop(url, strPrivate, strPublic)

    # access api endpoints using python request lib
    headers = {
    'X-Authorization': popTok,
    'Authorization': 'Bearer '+ accessTok,
    }

    response = requests.request("GET", url, headers=headers)
    # print(response.text)
    return json.loads(response.text)
