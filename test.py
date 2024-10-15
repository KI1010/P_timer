import tkinter as tk

root = tk.Tk()
root.geometry("+0+0")  # ウィンドウの位置を設定
root.overrideredirect(True)  # タイトルバーやボーダーを削除

label = tk.Label(root, text="Hello, World!", bg="lightblue")
label.pack(fill=tk.BOTH, expand=True)

root.mainloop()