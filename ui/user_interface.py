import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import webbrowser

class MinecraftLauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Minecraft Launcher")
        self.geometry("1200x700")
        self.configure(bg='#2C2F33')  # 窗口背景設置為深色

        # 左側導航欄
        self.left_frame = tk.Frame(self, bg='black', width=200)
        self.left_frame.pack(side='left', fill='y')

        # 帳號下拉選單
        self.account_var = tk.StringVar()
        self.account_menu = ttk.Combobox(self.left_frame, textvariable=self.account_var, state='readonly')
        self.account_menu['values'] = ['TunaDaddy4993', 'Microsoft 帳號']
        self.account_menu.current(0)
        self.account_menu.pack(pady=10, padx=10)

        self.add_left_button("Home", "white", "green", self.show_start_tab)

        # 中間主內容區
        self.main_frame = tk.Frame(self, bg='#2C2F33')  # 主框架背景設置為深色
        self.main_frame.pack(side='left', fill='both', expand=True)

        # 創建 Notebook
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill='both', expand=True, pady=10)

        # 創建分頁
        self.create_tabs()

        # 左下角
        self.left_bottom_frame = tk.Frame(self.left_frame, bg='black')
        self.left_bottom_frame.pack(side='bottom', fill='x', pady=10)

        self.add_left_bottom_label("設定", "white")
        self.add_left_bottom_label_with_link("有什麼新內容?", "white", "https://www.minecraft.net/zh-hant")

        # 版本資訊
        self.version_var = tk.StringVar()
        self.version_menu = ttk.Combobox(self.main_frame, textvariable=self.version_var, state='readonly')
        self.version_menu['values'] = ['1.20.4', '1.20.3', '1.20.2']
        self.version_menu.current(0)
        self.version_menu.pack(side='bottom', anchor='sw', padx=10, pady=10)

    def add_left_button(self, text, fg, bg, command):
        button = tk.Button(self.left_frame, text=text, fg=fg, bg=bg, font=("Arial", 14), command=command)
        button.pack(pady=5, padx=10, anchor='w')

    def add_left_bottom_label_with_link(self, text, fg, link):
        label = tk.Label(self.left_bottom_frame, text=text, fg=fg, bg='black', font=("Arial", 14), cursor="hand2")
        label.pack(pady=5, padx=10, anchor='w')
        label.bind("<Button-1>", lambda e: self.open_link(link))
    def add_left_bottom_label(self, text, fg, bg='black'):
        label = tk.Label(self.left_bottom_frame, text=text, fg=fg, bg=bg, font=("Arial", 14))
        label.pack(pady=5, padx=10, anchor='w')
    def open_link(self, link):
        webbrowser.open_new(link)

    def create_tabs(self):
        # 樣式設置
        style = ttk.Style()
        style.theme_create("dark", parent="alt", settings={
            "TNotebook": {
                "configure": {"background": "#2C2F33"}
            },
            "TNotebook.Tab": {
                "configure": {"background": "#2C2F33", "foreground": "white", "font": ("Arial", 16)},  # 增加字體大小
                "map": {"background": [("selected", "#4CAF50")], "foreground": [("selected", "white")]}
            }
        })
        style.theme_use("dark")

        # 開始遊戲分頁
        self.start_tab = tk.Frame(self.notebook, bg='#2C2F33')
        self.notebook.add(self.start_tab, text='開始遊戲')
        # 加載並顯示圖片
        self.image_path = "D:/python2/window_project/mc-launcher/minecraft/test_2.png"  # 替換為您的圖片路徑
        self.image = Image.open(self.image_path)
        self.photo = ImageTk.PhotoImage(self.image)
        
        start_image_label = tk.Label(self.start_tab, image=self.photo, bg='#2C2F33')
        start_image_label.pack(pady=20)

        # 開始遊戲按鈕
        start_button = tk.Button(self.start_tab, text="開始遊戲", bg='#4CAF50', fg='white', font=("Arial", 16))
        start_button.pack(pady=10)

        # 安裝檔分頁
        self.install_tab = tk.Frame(self.notebook, bg='#2C2F33')
        self.notebook.add(self.install_tab, text='安裝檔')
        self.create_install_tab()

        # 外觀分頁
        appearance_tab = tk.Frame(self.notebook, bg='#2C2F33')
        self.notebook.add(appearance_tab, text='外觀')
        appearance_label = tk.Label(appearance_tab, text="外觀分頁", bg='#2C2F33', fg='white', font=("Arial", 18))
        appearance_label.pack(pady=20)

    def create_install_tab(self):

        header_frame = tk.Frame(self.install_tab, bg='#2C2F33')
        header_frame.pack(pady=20, padx=10, fill='x')

        # 搜尋標題及搜尋框
        search_frame = tk.Frame(header_frame, bg='#2C2F33')
        search_frame.pack(side='left', padx=10)

        search_label = tk.Label(search_frame, text="搜尋", bg='#2C2F33', fg='white', font=("Arial", 16, "bold"))
        search_label.pack(anchor='w')

        search_entry = tk.Entry(search_frame, bg='white', fg='black', font=("Arial", 12))
        search_entry.pack(anchor='w')

        # 排序方式標題及下拉選單
        sort_frame = tk.Frame(header_frame, bg='#2C2F33')
        sort_frame.pack(side='left', padx=10)

        sort_label = tk.Label(sort_frame, text="排序方式", bg='#2C2F33', fg='white', font=("Arial", 16, "bold"))
        sort_label.pack(anchor='w')

        sort_options = ['最近一次遊玩', '按名稱', '按大小']
        sort_var = tk.StringVar()
        sort_dropdown = ttk.Combobox(sort_frame, textvariable=sort_var, values=sort_options, state='readonly')
        sort_dropdown.current(0)
        sort_dropdown.pack(anchor='w')

        # 版本標題及選項
        version_frame = tk.Frame(header_frame, bg='#2C2F33')
        version_frame.pack(side='left', padx=10)

        version_label = tk.Label(version_frame, text="版本", bg='#2C2F33', fg='white', font=("Arial", 16, "bold"))
        version_label.pack(anchor='w')

        versions_frame = tk.Frame(version_frame, bg='#2C2F33')
        versions_frame.pack(anchor='w')

        versions = ['正式版', '快照版', '模組']
        self.version_vars = [tk.IntVar() for _ in range(len(versions))]
        for i, version in enumerate(versions):
            checkbox = tk.Checkbutton(versions_frame, text=version, variable=self.version_vars[i], bg='#2C2F33', fg='white', font=("Arial", 12), onvalue=1, offvalue=0)
            checkbox.pack(side='left', padx=5)

        # 模擬顯示安裝檔列表
        install_list_frame = tk.Frame(self.install_tab, bg='#2C2F33')
        install_list_frame.pack(pady=20, fill='x')

        install_list_frame = tk.Frame(self.install_tab, bg='#2C2F33')
        install_list_frame.pack(pady=20)

        # 模擬安裝檔列表
        installs = [
            {"version": "1.20.4", "type": "正式版"},
            {"version": "最新版本", "type": "1.20.6"},
            {"version": "1.20.1 fabric", "type": "fabric-loader-0.15.7-1.20.1"},
            {"version": "fabric-loader-1.20.1", "type": "fabric-loader-0.15.7-1.20.1"},
            {"version": "1.18.2", "type": "1.18.2"},
            {"version": "forge", "type": "1.12.2-forge-14.23.5.2859"},
        ]

        for install in installs:
            install_frame = tk.Frame(install_list_frame, bg='#2C2F33')
            install_frame.pack(fill='x', pady=5)

            version_label = tk.Label(install_frame, text=install["version"], bg='#2C2F33', fg='white', font=("Arial", 16, "bold"))
            version_label.pack(anchor='w')

            type_label = tk.Label(install_frame, text=install["type"], bg='#2C2F33', fg='white', font=("Arial", 12))
            type_label.pack(anchor='w')

            separator = tk.Frame(install_list_frame, bg='#2C2F33', height=2, bd=1, relief='sunken')
            separator.pack(fill='x', pady=5)



    def show_start_tab(self):
        self.notebook.select(self.start_tab)

    def show_install_tab(self):
        self.notebook.select(self.install_tab)

if __name__ == "__main__":
    app = MinecraftLauncherApp()
    app.mainloop()