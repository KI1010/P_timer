import tkinter as tk
import time

root = tk.Tk()

class app:
    def __init__(self,root):
        self.root = root
        self.title = root.title("タイマー")
        self.geometry = root.geometry("500x300+0+0")
        self.timer = 1  #タイマー時間
        self.pose_limit = 1 #ポーズ中リセットまでのタイムリミット
        self.pose_id = None
        self.root.resizable(False,False)
        self.state_pose = False
        self.now_count = None
        self.after_id = None

        #ウィジェット
        self.label = tk.Label(root, text="タイマー", bg="black", fg="white", font=("Helvetica",25),width=10)
        self.label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame = tk.Frame(self.root)
        self.frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.button = tk.Button(self.frame,text="スタート",command=self.start_timer,font=("Helvetica",20))
        self.button.pack(side=tk.LEFT,fill=tk.BOTH, expand=True)
        self.button2 = tk.Button(self.frame,text="ストップ",font=("Helvetica",20),state=tk.DISABLED, command=self.stop_timer)
        self.button2.pack(side=tk.RIGHT,fill=tk.BOTH, expand=True)
        
    def start_timer(self):  #スタートボタン機能
        if self.state_pose:
            self.restart()
        else:
            self.countDown(self.timer*60)
            self.toggle_button_label("counting")

    def stop_timer(self):   #ストップボタン機能
        #タイマーが動いている場合ストップ  関数化する
        if self.after_id is not None:
            self.state_pose = True
            self.toggle_button_label("posed")
            self.root.after_cancel(self.after_id)
            self.after_id = None
            self.posed(self.pose_limit*60)
        #もう一度押すとリセット 関数化する
        else:
            self.state_pose = None
            self.toggle_button_label("reset")
            self.now_count = None
            self.root.after_cancel(self.pose_id)
            self.after_id = None

    #一時停止の処理
    def posed(self,pose_count):
        if pose_count > 0:
            if pose_count % 2 == 0:
                mins,secs = divmod(self.now_count,60)
                timer = f"{mins:02}:{secs:02}"
                self.label["text"] = timer
            else:
                mins,secs = divmod(self.now_count,60)
                timer = f"{mins:02} {secs:02}"
                self.label["text"] = timer

            self.pose_id = self.root.after(1000,self.posed,pose_count -1)
        else:
            #リセットの処理あとで関数化する
            self.state_pose = None
            self.toggle_button_label("reset")
            self.now_count = None
            self.root.after_cancel(self.pose_id)
            self.after_id = None
        
            
    #カウントダウン機能
    def countDown(self,total_seconds):
        if total_seconds > 0:
            mins,secs = divmod(total_seconds,60)
            timer = f"{mins:02}:{secs:02}"
            self.label["text"] = timer
            self.now_count = total_seconds
            self.after_id = self.root.after(1000,self.countDown,total_seconds -1)
        else:
            #あとで修正
            print(f"{self.timer}分経過しました")
            self.label["text"] = "タイマー終了"
            self.button.config(state=tk.NORMAL)
    
    #タイマーを再開する機能
    def restart(self):
        self.toggle_button_label("counting")
        self.state_pose = False
        self.countDown(self.now_count)
        self.root.after_cancel(self.pose_id)

    def toggle_button_label(self,mode):
        match mode:
            case "posed":
                self.button["text"] = "　再開　"
                self.button2["text"] = "リセット"
                self.button.config(state=tk.NORMAL)
                self.button2.config(state=tk.NORMAL)
            case "counting":
                self.button["text"] = "スタート"
                self.button2["text"] = "ストップ"
                self.button.config(state=tk.DISABLED)
                self.button2.config(state=tk.NORMAL)
            case "reset":
                self.label["text"] = "タイマー"
                self.button["text"] = "スタート"
                self.button2["text"] = "ストップ"
                self.button.config(state=tk.NORMAL)
                self.button2.config(state=tk.DISABLED)

App = app(root)
root.mainloop()