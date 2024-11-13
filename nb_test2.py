import tkinter as tk
from tkinter import ttk

root = tk.Tk()

# Notebookウィジェットの作成
notebook = ttk.Notebook(root)

# スクロール可能なフレームを作成
def create_scrollable_frame(parent):
    canvas = tk.Canvas(parent)
    scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    frame = ttk.Frame(canvas)

    # スクロール可能なフレームをCanvasに設定
    canvas.create_window((0, 0), window=frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # スクロールバーとCanvasを配置
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    frame.bind(
        "<Configure>", 
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    return frame, canvas

# タブ1 (スクロール可能な設定内容)
tab1 = ttk.Frame(notebook)
frame1, canvas1 = create_scrollable_frame(tab1)
notebook.add(tab1, text="General")

# タブ1にスクロール可能な設定項目を追加
for i in range(10):
    label = ttk.Label(frame1, text=f"Setting Item {i+1}")
    label.pack(padx=10, pady=5)

# タブ1にボタンを追加
def on_button_click():
    print("Button clicked!")

button = ttk.Button(frame1, text="Save Settings", command=on_button_click)
button.pack(padx=10, pady=20)

# タブ2 (スクロール可能な設定内容)
tab2 = ttk.Frame(notebook)
frame2, canvas2 = create_scrollable_frame(tab2)
notebook.add(tab2, text="Display")

# タブ2にスクロール可能な設定項目を追加
for i in range(10):
    label = ttk.Label(frame2, text=f"Display Setting {i+1}")
    label.pack(padx=10, pady=5)

# タブ2にボタンを追加
def on_display_button_click():
    print("Display Settings Saved!")

display_button = ttk.Button(frame2, text="Save Display Settings", command=on_display_button_click)
display_button.pack(padx=10, pady=20)

# Notebookを配置
notebook.pack(padx=10, pady=10, expand=True, fill="both")

root.mainloop()
