import tkinter as tk

root = tk.Tk()
root.geometry("400x200")

# タイトルバーを非表示に
root.overrideredirect(True)

# カスタムタイトルバー
title_bar = tk.Frame(root, bg="yellow", relief="raised", bd=2)
title_bar.pack(side="top", fill="x")

# タイトルラベル
title_label = tk.Label(title_bar, text="Custom Title Bar", bg="yellow")
title_label.pack(side="left", padx=10)

# ウィンドウのコンテンツ
content = tk.Frame(root)
content.pack(expand=True, fill="both")

# ウィンドウを移動できるようにする
def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

title_bar.bind("<B1-Motion>", move_window)

root.mainloop()
