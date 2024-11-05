import tkinter as tk
from tkinter import ttk

# メインウィンドウの作成
root = tk.Tk()
root.title("スクロール表示の例")

# Treeviewウィジェットの作成
tree = ttk.Treeview(root, columns=("col1", "col2"), show='headings')
tree.heading("col1", text="列1")
tree.heading("col2", text="列2")

# 列の幅を設定
tree.column("col1", width=100, anchor='w')  # 列1を左寄せ
tree.column("col2", width=100, anchor='w')  # 列2を左寄せ

# スクロールバーの作成
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

# ウィジェットの配置
tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)  # Treeviewを左側に
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)            # スクロールバーを右側に

# サンプルデータの挿入
for i in range(50):  # 50行のデータを作成
    tree.insert("", "end", values=(f"データ {i+1}", f"値 {i*10}"))

# メインループを開始
root.mainloop()
