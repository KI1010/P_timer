import tkinter as tk
from tkinter import ttk

class ColorSwitcherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Color Mode Switcher")
        self.root.geometry("400x300")

        # ライトモードとダークモードの色設定
        self.light_mode = {
            "bg": "#f5f5f5", 
            "text": "#333333", 
            "button_bg": "#3498db", 
            "button_fg": "#ffffff",
            "accent": "#f39c12"
        }
        
        self.dark_mode = {
            "bg": "#2c3e50", 
            "text": "#ecf0f1", 
            "button_bg": "#1abc9c", 
            "button_fg": "#ffffff",
            "accent": "#e74c3c"
        }

        # 初期状態: ライトモード
        self.current_mode = self.light_mode
        
        # モード切替ボタン
        self.toggle_button = tk.Button(self.root, text="Switch to Dark Mode", command=self.toggle_mode)
        self.toggle_button.pack(pady=20)

        # ラベル
        self.label = tk.Label(self.root, text="Welcome to the App!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        # アクションボタン
        self.action_button = tk.Button(self.root, text="Click Me!", bg=self.current_mode["button_bg"], fg=self.current_mode["button_fg"])
        self.action_button.pack(pady=20)

        # 色を適用
        self.apply_colors()

    def apply_colors(self):
        """現在のモードに基づいて色を適用"""
        self.root.config(bg=self.current_mode["bg"])
        self.label.config(bg=self.current_mode["bg"], fg=self.current_mode["text"])
        self.action_button.config(bg=self.current_mode["button_bg"], fg=self.current_mode["button_fg"])

    def toggle_mode(self):
        """ライトモードとダークモードを切り替え"""
        if self.current_mode == self.light_mode:
            self.current_mode = self.dark_mode
            self.toggle_button.config(text="Switch to Light Mode")
        else:
            self.current_mode = self.light_mode
            self.toggle_button.config(text="Switch to Dark Mode")
        
        # 色を適用
        self.apply_colors()

# Tkinterのウィンドウを作成
root = tk.Tk()
app = ColorSwitcherApp(root)
root.mainloop()
