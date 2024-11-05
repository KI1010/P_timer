import tkinter as tk

root = tk.Tk()

# フレームを作成して、ListboxとScrollbarを含む
frame = tk.Frame(root)
frame.pack()

# Listboxウィジェットを作成
listbox = tk.Listbox(frame, height=10, width=40)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# スクロールバーを作成し、Listboxにリンクさせる
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# スクロールバーのコントロールをListboxに設定
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Listboxにサンプルデータを追加
for i in range(100):
    listbox.insert(tk.END, f"Item {i+1}")

root.mainloop()
