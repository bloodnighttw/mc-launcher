# import tkinter as tk
# import webview
# import threading

# import http.server
# import socketserver
# import os

# class SkinWin():

#     def __init__(self, skin_name):
#         self.skin_name = skin_name
#         self.port = 3001

#         with open("skin/3D-Minecraft-Skin-Viewer-master/index.html", "r") as file:
#             lines = file.readlines()
#         lines[201] = "img.src = 'http://localhost:3001/" + skin_name + "';\n"
#         with open("skin/3D-Minecraft-Skin-Viewer-master/index.html", "w") as file:
#             file.writelines(lines)
#         # for line in lines:
#         #     print(line, end="")

#         server_thread = threading.Thread(target=self.start_server, daemon=True)
#         server_thread.start()

#         self.window = webview.create_window(
#                 "View Skin", "skin/3D-Minecraft-Skin-Viewer-master/index.html"
#             )
#         webview.start()

#     def start_server(self):
#         web_dir = os.path.join(os.path.dirname(__file__), "skins")
#         os.chdir(web_dir)
#         with socketserver.TCPServer(("", self.port), MyHTTPRequestHandler) as httpd:
#             print(f"Serving on port {self.port}")
#             httpd.serve_forever()

# # Create an HTTP request handler class
# class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
#     def end_headers(self):
#         self.send_header("Access-Control-Allow-Origin", "*")
#         self.send_header("Access-Control-Allow-Methods", "GET")
#         self.send_header("Access-Control-Allow-Headers", "Content-Type")
#         super().end_headers()

# class WebWindow(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         # Source from https://github.com/earthiverse/3D-Minecraft-Skin-Viewer
#         self.window = webview.create_window(
#             "View Skin", "3D-Minecraft-Skin-Viewer-master/index.html"
#         )
#         webview.start()

# # test = SkinWin("0ac346c7ace6165c.png")



import os
import threading
import http.server
import socketserver
import socket
import tkinter as tk
import webview

class SkinWin():
    def __init__(self, skin_name):
        self.skin_name = skin_name
        self.port = 3001

        # Modify the HTML file to include the skin image
        with open("skin/3D-Minecraft-Skin-Viewer-master/index.html", "r") as file:
            lines = file.readlines()
        lines[201] = f"img.src = 'http://localhost:{self.port}/{skin_name}';\n"
        with open("skin/3D-Minecraft-Skin-Viewer-master/index.html", "w") as file:
            file.writelines(lines)

        # Start the server in a new thread
        if self.is_port_available(self.port):
            server_thread = threading.Thread(target=self.start_server, daemon=True)
            server_thread.start()

        # Create the webview window
        self.window = webview.create_window(
            "View Skin", "skin/3D-Minecraft-Skin-Viewer-master/index.html"
        )
        webview.start()
    
    def is_port_available(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('localhost', port)) != 0

    def start_server(self):
        handler = lambda *args, **kwargs: MyHTTPRequestHandler(self.skin_name, *args, **kwargs)
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"Serving on port {self.port}")
            httpd.serve_forever()

# Create an HTTP request handler class
class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, skin_name, *args, **kwargs):
        self.skin_name = skin_name
        super().__init__(*args, **kwargs)

    def translate_path(self, path):
        # Serve files from the "skins" directory
        web_dir = os.path.join(os.path.dirname(__file__), "skins")
        path = os.path.normpath(http.server.SimpleHTTPRequestHandler.translate_path(self, path))
        relpath = os.path.relpath(path, os.getcwd())
        print(os.path.join(web_dir, relpath))
        return os.path.join(web_dir, relpath)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

# Example usage
# test = SkinWin("0ac346c7ace6165c.png")
