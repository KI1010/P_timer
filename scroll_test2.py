import tkinter as tk

root = tk.Tk()

# フレームを作成して、TextとScrollbarを含む
frame = tk.Frame(root)
frame.pack()

# Textウィジェットを作成
text_widget = tk.Text(frame, height=10, width=40)
text_widget.pack(side=tk.LEFT, fill=tk.BOTH)

# スクロールバーを作成し、Textウィジェットにリンクさせる
scrollbar = tk.Scrollbar(frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# スクロールバーのコントロールをTextウィジェットに設定
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

# Textウィジェットにサンプルデータを追加
sample_text = "\n".join([f"Line {i+1}" for i in range(100)])
text_widget.insert(tk.END, sample_text)

root.mainloop()
