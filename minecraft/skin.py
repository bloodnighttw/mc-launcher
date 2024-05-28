import time

import requests

from minecraft.auth import generate_device_code, exchange_device_code, xbox_live_authenticate, xbox_security_token, \
    get_minecraft_token, check_minecraft_profile

MINECRAFT_UPLOAD_SKIN = "https://api.minecraftservices.com/minecraft/profile/skins"
MINECRAFT_RESET_SKIN = "https://api.minecraftservices.com/minecraft/profile/skins/active"


# https://wiki.vg/Mojang_API#Upload_Skin
def upload_skin(token, filepath):
    bearer = f"Bearer {token}"
    header = {
        "Authorization": bearer,
    }
    skin = open(filepath, 'rb').read()
    files = {
        'variant': (None, 'classic'),
        'file': ('steeevee.png', skin, 'image/png'),
    }

    response = requests.post(MINECRAFT_UPLOAD_SKIN, headers=header, files=files)
    return response.json()


# https://wiki.vg/Mojang_API#Reset_Skin
def reset_skin(token):
    bearer = f"Bearer {token}"
    header = {
        "Authorization": bearer,
    }
    response = requests.delete(MINECRAFT_RESET_SKIN, headers=header)
    return response.json()


if __name__ == "__main__":
    a = generate_device_code()
    print(f"Please go to {a['verification_uri']} and enter {a['user_code']} to authenticate")
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
    g = upload_skin(e["access_token"], "../testfile/test.png")
    print(g)
    h = reset_skin(e["access_token"])
    print(h)
