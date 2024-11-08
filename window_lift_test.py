import tkinter as tk
from tkinter import colorchooser

def choose_color():
    # ウィンドウBをウィンドウAの前に表示
    window_b.lift()
    
    # カラーピッカーを開く
    colorchooser.askcolor()

root = tk.Tk()
root.geometry("300x100")
root.title("メインウィンドウ")

# ウィンドウAの設定
window_a = tk.Toplevel(root)
window_a.geometry("300x100+50+200")
window_a.title("ウィンドウA")

# ウィンドウBの設定
window_b = tk.Toplevel(root)
window_b.geometry("300x100+100+300")
window_b.title("ウィンドウB")

# ボタンの設定
button = tk.Button(root, text="色選択", command=choose_color)
button.pack(pady=20)

root.mainloop()
