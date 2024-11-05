import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self, root):
        self.style = ttk.Style()
        self.style.theme_use("clam")  # テーマの設定

        # カスタムスタイルの設定
        self.style.configure("MyApp.PrimaryButton.TButton", 
                             padding=10, 
                             background="blue", 
                             foreground="white")

        # スタイルを適用したボタンの作成
        self.button = ttk.Button(root, text="Primary Button", style="MyApp.PrimaryButton.TButton")
        self.button.pack(pady=20)

# Tkinterアプリの実行
root = tk.Tk()
app = MyApp(root)
root.mainloop()
