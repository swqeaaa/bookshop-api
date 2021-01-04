from itsdangerous import TimedJSONWebSignatureSerializer as TJWSS, SignatureExpired, BadData
import time



def MakeCode(username):
    salt = "xSrIG63Ov0dg"
    payload = {
        "username": "",
    }
    tjwss = TJWSS(salt, 10000)
    payload['username'] = username
    token = tjwss.dumps(payload).decode()
    return token

def Decode(token):
    salt = "xSrIG63Ov0dg"
    tjwss = TJWSS(salt, 10000)
    try:
        data = tjwss.loads(token)
        return data
    except :
        return -1
