## 各位不要慌，分工

1. UI: 靜態介面、選單、按鈕、網址連結、美術修改: 王永明
2. UI: 登入頁面更動、skin preview、更改字體、進度條: 侯有鍵
3. 獲取官方內容: 帳號登入、取得與上傳skin、取得log: 李弘唯
4. 啟動MC/切換版本: 控制執行緒啟動不同版本: 許振維

##### 筆記

- [報告鏈接](https://docs.google.com/presentation/d/112dPtY5mKqVvaQrIk79BKTkvZOtf3zyT7nGj-qk0eAk/edit?usp=sharing)

- 跑 `index.py` 開始程式

- 視窗本體在 `/ui` 資料夾，編輯各自負責的頁面即可。別亂編輯別人的部分。影響merge

- `/example ` 資料夾有我們上課學過的所有功能，執行`uiexample.py`參考套件如何用

- 在`pagex.py`裏呼叫 `main.logging` 來顯示debug資訊；`main.settings`來記錄設定

#####  執行

先確認已經安裝好以下模組

    pip install --user pywebview

再執行 `/mc-launcher/index.py`

###### Source Citing

Skin Viewer: https://github.com/earthiverse/3D-Minecraft-Skin-Viewer
Skins: https://namemc.com/minecraft-skins
Minecraft Font: https://www.fontspace.com/category/minecraft (Free for personal use)