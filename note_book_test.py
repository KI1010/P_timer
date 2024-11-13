import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Notebookウィジェットの作成
notebook = ttk.Notebook(root)

# タブを作成
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
notebook.add(tab1, text="General")
notebook.add(tab2, text="Display")

# タブ内にボタンやラベルを追加
label1 = ttk.Label(tab1, text="General settings here")
label1.pack(padx=20, pady=20)

label2 = ttk.Label(tab2, text="Display settings here")
label2.pack(padx=20, pady=20)

notebook.pack(padx=10, pady=10)

root.mainloop()