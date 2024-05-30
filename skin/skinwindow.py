import os
import threading
import http.server
import socketserver
import socket
import webview


class SkinWin:
    def __init__(self, skin_name):
        self.skin_name = skin_name
        self.PORT = 3001
        self.HTML_FILE = "skin/3D-Minecraft-Skin-Viewer-master/index.html"

        # Modify the HTML file to include the skin image
        with open(self.HTML_FILE, "r") as file:
            lines = file.readlines()
        lines[201] = f"img.src = 'http://localhost:{self.PORT}/{skin_name}';\n"
        with open(self.HTML_FILE, "w") as file:
            file.writelines(lines)

        # Start the server in a new thread
        if self.is_port_available(self.PORT):
            server_thread = threading.Thread(target=self.start_server, daemon=True)
            server_thread.start()

        # Create the webview window
        self.window = webview.create_window("View Skin", self.HTML_FILE)
        webview.start()

    def is_port_available(self, port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) != 0

    def start_server(self):
        handler = lambda *args, **kwargs: MyHTTPRequestHandler(
            self.skin_name, *args, **kwargs
        )
        with socketserver.TCPServer(("", self.PORT), handler) as httpd:
            print(f"Serving on port {self.PORT}")
            httpd.serve_forever()

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, skin_name, *args, **kwargs):
        self.skin_name = skin_name
        super().__init__(*args, **kwargs)

    def translate_path(self, path):
        # __file__ is in 'mc-launcher/skin/' directory
        web_dir = os.path.join(os.path.dirname(__file__), "skins")
        path = os.path.normpath(
            http.server.SimpleHTTPRequestHandler.translate_path(self, path)
        )
        relpath = os.path.relpath(path, os.getcwd())
        print(os.path.join(web_dir, relpath))
        return os.path.join(web_dir, relpath)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()