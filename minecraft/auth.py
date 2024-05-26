import time

import requests

client_id = "47f3e635-2886-4628-a1c2-fd8a9f4d7a5f"
DEVICECODE_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/devicecode"
TOKEN_URL = "https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
MINECRAFT_LOGIN_WITH_XBOX = "https://api.minecraftservices.com/authentication/login_with_xbox"
XBOX_USER_AUTHENTICATE = "https://user.auth.xboxlive.com/user/authenticate"
XBOX_XSTS_AUTHORIZE = "https://xsts.auth.xboxlive.com/xsts/authorize"
MINECRAFT_PROFILE = "https://api.minecraftservices.com/minecraft/profile"
SCOPE = "XboxLive.signin offline_access"
GRANT_TYPE = "urn:ietf:params:oauth:grant-type:device_code"
header = {
    "Content-Type": "application/x-www-form-urlencoded"
}


def generate_device_code():
    data = {
        "client_id": client_id,
        "scope": SCOPE
    }
    response = requests.post(DEVICECODE_URL, data=data, headers=header)
    return response.json()


# Exchange device code for access token
# Returns three errors response and 1 success response.
# If the user has not yet authenticated the device code, the response will be:
# {
#     "error": "authorization_pending",
#     ......
# }
# If the user has denied the device code, the response will be:
# {
#     "error": "authorization_declined",
#     ......
# }
# If the device code has expired, the response will be:
# {
#     "error": "expired_token",
#     ......
# }
# If the device code is valid and the user has authenticated it, the response will be:
# {
#     "token_type": "Bearer",


def exchange_device_code(device_code):
    data = {
        "client_id": client_id,
        "device_code": device_code,
        "grant_type": GRANT_TYPE
    }
    response = requests.post(TOKEN_URL, data=data, headers=header)
    return response.json()


def xbox_live_authenticate(token):
    data = {
        "Properties": {
            "AuthMethod": "RPS",
            "SiteName": "user.auth.xboxlive.com",
            "RpsTicket": f"d={token}"
        },
        "RelyingParty": "http://auth.xboxlive.com",
        "TokenType": "JWT"
    }
    response = requests.post(XBOX_USER_AUTHENTICATE, json=data)
    return response.json()


def xbox_security_token(token):
    data = {
        "Properties": {
            "SandboxId": "RETAIL",
            "UserTokens": [token]
        },
        "RelyingParty": "rp://api.minecraftservices.com/",
        "TokenType": "JWT"
    }
    response = requests.post(XBOX_XSTS_AUTHORIZE, json=data)
    return response.json()


def get_minecraft_token(uhs, token):
    header_ = {
        "Content-Type": "application/json"
    }

    data_ = {
        "identityToken": "XBL3.0 x={};{}".format(int(uhs), token)
    }
    print(data_)
    response = requests.post(MINECRAFT_LOGIN_WITH_XBOX, json=data_, headers=header_)
    return response.json()


# Response be like:
# {
#   'id': '280796c9bf944abd98bbf0b89be44d76',
#   'name': 'bloodnighttw',
#   'skins': [
#       {
#           'id':  'bccda79a-27a3-4183-89b4-7bc7ae1cf662',
#           'state': 'ACTIVE',
#           'url': 'http://textures.minecraft.net/texture/5d73e301eb4323b678a24dd3d6c26239d86d796bc28989c9eb3e02436115f12c',
#           'textureKey': '5d73e301eb4323b678a24dd3d6c26239d86d796bc28989c9eb3e02436115f12c',
#           'variant': 'CLASSIC'
#       }
#   ],
#   'capes': [
#       {
#           'id': '7412868d-7be3-429f-b629-ed5074d2455c', 'state': 'INACTIVE',
#           'url': 'http://textures.minecraft.net/texture/f9a76537647989f9a0b6d001e320dac591c359e9e61a31f4ce11c88f207f0ad4',
#           'alias': 'Vanilla'
#       }, ......
#   ],
#   'profileActions': {}
#   }
#
# If the user has not owned Minecraft, the response will not return 200
def check_minecraft_profile(token):
    header = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(MINECRAFT_PROFILE, headers=header)
    return response.json()



if __name__ == "__main__":
    a = generate_device_code()
    print(a)
    b = None
    while True:
        b = exchange_device_code(a["device_code"])
        if "error" in b:
            if b["error"] == "authorization_pending":
                time.sleep(a["interval"])  # Wait for the user to authenticate next loop
            elif b["error"] == "authorization_declined":
                print("Authorization declined")  # Failed
                break
            elif b["error"] == "expired_token":
                print("Expired token")  # Failed
                break
        else:
            break  # Success

    print(b["access_token"])
    c = xbox_live_authenticate(b["access_token"])
    print(c)
    d = xbox_security_token(c["Token"])
    print(d)
    print(d["DisplayClaims"]["xui"][0]["uhs"])
    e = get_minecraft_token(d["DisplayClaims"]["xui"][0]["uhs"], d["Token"])
    print(e)
    f = check_minecraft_profile(e["access_token"])  # if not owned minecraft, it will not return 200
    print(f)
