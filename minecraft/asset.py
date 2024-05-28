import concurrent.futures
import json
import os
import platform
import urllib.request

import requests


# https://wiki.vg/Game_files#Game
# version list
# Return example:
# {
#     "latest": {
#         "release": "1.17.1",
#         "snapshot": "21w37a"
#     },
#     "versions": [
#         {
#             "id": "1.17.1",
#             "type": "release",
#             "url": "https://launchermeta.mojang.com/v1/packages/2c3e9a9f1c0d8d8d7c7f2b8b6b0c8f1b9b6f2e7d/1.17.1.json",
#             "time": "2021-07-06T14:00:00+00:00",
#             "releaseTime": "2021-07-06T14:00:00+00:00",
#             "sha1": "2c3e9a9f1c0d8d8d7c7f2b8b6b0c8f1b9b6f2e7d",   # The hash of the version file
#             "complianceLevel": 1
#         },......
#     ]
# }
def get_all_version():
    response = requests.get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    return response.json()


def get_version_info(versions_data):
    response = requests.get(versions_data["url"])
    return response.json()


# https://wiki.vg/Game_files#Libraries
# Return List of url of libraries you need to download.
def get_libraries_download_list(version_info):
    temp = platform.system()
    os = ""
    if temp == "Windows":
        os = "windows"
    elif temp == "Darwin":
        os = "osx"
    elif temp == "Linux":
        os = "linux"

    download_list = []
    for i in version_info["libraries"]:
        if "rules" in i:
            if i["rules"][0]["action"] != "allow" or i["rules"][0]["os"]["name"] != os:
                continue

        url_and_path = {
            "url": i["downloads"]["artifact"]["url"],
            "path": f"libraries/{i['downloads']['artifact']['path']}"
        }
        download_list.append(url_and_path)

    return download_list


def get_index_list(version_info):
    response = requests.get(version_info["assetIndex"]["url"])
    return response.json()


# https://wiki.vg/Game_files#Assets
# Return List of url and path of assets you need to download and store in.
# Note: This is not support 1.7 and below.
def get_asset_list(indexes):
    download_list = []
    for i in indexes["objects"].values():
        sha1 = i["hash"]
        fullname = f"{sha1[:2]}/{sha1}"
        url_and_path ={
            "url": f"https://resources.download.minecraft.net/{fullname}",
            "path": f"assets/objects/{fullname}"
        }
        download_list.append(url_and_path)
    return download_list


def get_client_url(version):
    response = requests.get(version["url"]).json()
    return response["downloads"]["client"]["url"]


# only for test
def download(i):
    if not os.path.exists(os.path.dirname(f"temp/{i['path']}")):
        os.makedirs(os.path.dirname(f"temp/{i['path']}"))
    elif os.path.exists(f"temp/{i['path']}"):
        return
    print(f"Download {i['url']} to temp/{i['path']}")
    urllib.request.urlretrieve(i["url"], f"temp/{i['path']}")


# A small download function and a simple minecraft launcher, just for testing!
if __name__ == "__main__":
    a = get_all_version()
    print(a["versions"][0])
    test = {
        "id": "1.20.4",
        "type": "release",
        "url": "https://piston-meta.mojang.com/v1/packages/d6ebb22e7eeefd88f1cef6b32bcffcccf4326404/1.20.4.json",
        "time": "2024-05-22T06:20:02+00:00",
        "releaseTime": "2023-12-07T12:56:20+00:00",
        "sha1": "d6ebb22e7eeefd88f1cef6b32bcffcccf4326404",
        "complianceLevel": 1
    }
    version = get_version_info(test)
    b = get_libraries_download_list(version)
    indexes = get_index_list(version)
    if not os.path.exists("temp/assets/indexes"):
        os.makedirs("temp/assets/indexes")
    with open(f"temp/assets/indexes/{version['assetIndex']['id']}.json", "w") as f:
        f.write(json.dumps(indexes))
    c = get_asset_list(indexes)
    client_url = get_client_url(test)

    with concurrent.futures.ThreadPoolExecutor(max_workers=11) as executor:  # Download multiple files is io bound, we can use ThreadPoolExecutor to speed up the download speed
        for i in b:
            executor.submit(download, i)
        for i in c:
            executor.submit(download, i)

    urllib.request.urlretrieve(client_url, f"temp/client.jar")

    classpath = ""
    for i in b:
        classpath += f"{i['path']}:"

    classpath += f"client.jar"
    native = "libraries"
    token = "Token not Provide"
    asset = ""

    os.chdir("temp")
    os.system(f"java "
              f"-Djava.library.path={native} "
              f"-Dorg.lwjgl.system.SharedLibraryExtractPath={native} "
              f"-cp {classpath} "
              f"net.minecraft.client.main.Main "
              f"--accessToken {token} "
              f"--version {test['id']} "
              f"--assetsDir {asset}"
              f"--assetIndex {12}")