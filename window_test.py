import tkinter as tk

def auto_close_message():
    message_window = tk.Toplevel(root)
    message_window.title("Auto Close Message")
    
    label = tk.Label(message_window, text="This message will disappear in 3 seconds")
    label.pack(padx=20, pady=20)
    
    # 3秒後にウィンドウを閉じる
    message_window.after(3000, message_window.destroy)

root = tk.Tk()
root.geometry("300x200")

button = tk.Button(root, text="Show Message", command=auto_close_message)
button.pack(pady=20)

root.mainloop()
