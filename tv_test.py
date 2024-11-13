import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Treeviewウィジェットの作成
treeview = ttk.Treeview(root)

# ツリー項目を追加
treeview.insert("", "end", "general", text="General Settings")
treeview.insert("general", "end", "language", text="Language")
treeview.insert("general", "end", "theme", text="Theme")

treeview.insert("", "end", "display", text="Display Settings")
treeview.insert("display", "end", "resolution", text="Resolution")

treeview.pack(padx=10, pady=10)

root.mainloop()