import tkinter as tk
from tkinter import ttk
from datetime import datetime

# グローバル変数
entries = []

def insert_data(date_str, col2_data):
    # 日付をdatetime型に変換
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    date_str = date_obj.strftime("%Y-%m-%d")  # 再び文字列に戻す

    # 同じ日付のエントリを検索
    same_date_entries = [entry for entry in entries if entry[0] == date_str]

    # 新しいエントリを追加
    if len(same_date_entries) == 0:
        # 同じ日付が存在しない場合、エントリを追加
        tree.insert("", "end", values=(date_str, col2_data))
    else:
        # 同じ日付が存在する場合、最初のエントリを除く日付を空白にする
        tree.insert("", "end", values=("", col2_data))  # 日付の欄を空白にする

    # entriesリストにエントリを追加
    entries.append((date_str, tree.get_children()[-1] if tree.get_children() else None))

def populate_tree():
    # 例としてデータを挿入
    insert_data("2024-10-23", "Data A")
    insert_data("2024-10-23", "Data B")  # 同じ日付
    insert_data("2024-10-24", "Data C")

root = tk.Tk()
tree = ttk.Treeview(root, columns=("Date", "Column 2"), show='headings')

# 列の見出しを設定
tree.heading("Date", text="Date")
tree.heading("Column 2", text="Column 2")

# 列の幅を設定
tree.column("Date", width=100)
tree.column("Column 2", width=100)

tree.pack()

# データを挿入
populate_tree()
print(entries)

root.mainloop()
