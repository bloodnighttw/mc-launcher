# 1. UI: 靜態介面、選單、按鈕、網址連結、美術修改: 王永明
# 2. UI: 登入頁面更動、skin preview、更改字體、進度條: 侯有鍵
# 3. 獲取官方內容: 帳號登入、取得與上傳skin、取得log: 李弘唯
# 4. 啟動MC/切換版本: 控制執行緒啟動不同版本: 許振維
import time
import webbrowser
from tkinter import Tk
from tkinter.messagebox import askyesno

import ui
import skin
from minecraft.asset import get_all_version
from minecraft.auth import generate_device_code, exchange_device_code, xbox_live_authenticate, xbox_security_token, \
    get_minecraft_token, check_minecraft_profile


def skin_preview(skin_name):
    skin_app = skin.SkinWin(skin_name=skin_name)


all_version = get_all_version()["versions"]
device_code = generate_device_code()
user_profile = None
token = None
profiles = None

if __name__ == "__main__":
    version_list = get_all_version()
    tempTk = Tk()
    print(f"Please go to {device_code['verification_uri']} and enter {device_code['user_code']} to authenticate")
    answer = askyesno("Note",f"Copy {device_code['user_code']} and paste in browser!", icon='info')
    if not answer:
        exit(0)
    webbrowser.open(device_code["verification_uri"])

    while True:
        b = exchange_device_code(device_code["device_code"])
        if "error" in b:
            if b["error"] == "authorization_pending":
                time.sleep(device_code["interval"])  # Wait for the user to authenticate next loop
            elif b["error"] == "authorization_declined":
                print("Authorization declined")  # Failed
                break
            elif b["error"] == "expired_token":
                print("Expired token")  # Failed
                break
        else:
            break  # Success
    c = xbox_live_authenticate(b["access_token"])
    print(c)
    d = xbox_security_token(c["Token"])
    print(d)
    e = get_minecraft_token(d["DisplayClaims"]["xui"][0]["uhs"], d["Token"])
    print(e)
    token = e["access_token"]
    print(token)
    profiles = check_minecraft_profile(e["access_token"])
    print(profiles)
    tempTk.destroy()
    app = ui.Main(skin_preview,token, profiles)
    app.mainloop()
