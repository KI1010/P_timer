import tkinter as tk
from tkinter import colorchooser

# カラー選択関数
def choose_color():
    # カラーダイアログを開き、色の選択結果を取得
    color_code = colorchooser.askcolor(title="色を選択してください")
    # 選択された色をラベルに表示
    if color_code[1]:  # color_code[1]は16進数表現の色コード
        color_label.config(text=f"選択された色: {color_code[1]}", bg=color_code[1])

# ウィンドウを作成
root = tk.Tk()
root.title("カラー選択")

# カラー選択ボタン
color_button = tk.Button(root, text="色を選択", command=choose_color)
color_button.pack(pady=10)

# 選択された色を表示するラベル
color_label = tk.Label(root, text="選択された色: ")
color_label.pack(pady=10)

# メインループ
root.mainloop()
