# 1. UI: 靜態介面、選單、按鈕、網址連結、美術修改: 王永明
# 2. UI: 登入頁面更動、skin preview、更改字體、進度條: 侯有鍵
# 3. 獲取官方內容: 帳號登入、取得與上傳skin、取得log: 李弘唯
# 4. 啟動MC/切換版本: 控制執行緒啟動不同版本: 許振維

import ui
import skin
def skin_preview(skin_name):
    skin_app = skin.SkinWin(skin_name=skin_name)
    # skin_app.mainloop()

if __name__ == "__main__":
    app = ui.Main(skin_preview)
    app.mainloop()
