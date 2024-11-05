import tkinter as tk

root = tk.Tk()

def ring_bell():
    root.bell()

button = tk.Button(root, text="Bell", command=ring_bell)
button.pack(pady=20)

root.mainloop()