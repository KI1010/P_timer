import tkinter as tk
from tkinter import messagebox

# Tkinterウィンドウの作成
root = tk.Tk()

# 通知を表示する関数
def show_notification():
    messagebox.showinfo("お知らせ", "これが通知です")

# ボタンを押したら通知を表示
button = tk.Button(root, text="通知を表示", command=show_notification)
button.pack(pady=20)

# メインループの開始
root.mainloop()
