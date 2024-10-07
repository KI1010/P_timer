import tkinter as tk
import time
from plyer import notification


root = tk.Tk()

class app:
    def __init__(self,root):
        self.root = root
        self.title = root.title("タイマー")
        self.geometry = root.geometry("300x200+0+0")
        self.timer = 1  #タイマー時間
        self.pose_limit = 1 #ポーズ中リセットまでのタイムリミット
        self.pose_id = None
        self.root.resizable(False,False)
        self.state_pose = False
        self.now_count = None
        self.after_id = None

        self.timer_display_width = int(1 * 300)
        self.timer_display_height = int(0.7 * 200)
        self.timer_button_width = int(0.5 * 300)
        self.timer_button_height = int(0.3 * 200)

        #ウィジェット
        self.label = tk.Label(root, text="タイマー", bg="black", fg="white", font=("Helvetica",25))
        #self.label.place(x=0, y=0, width=self.timer_display_width, height=self.timer_display_height)
        self.label.place(relx=0, rely=0, relwidth=1, relheight=0.7)
        self.button = tk.Button(root, text="スタート", command=self.start_timer, font=("Helvetica",20))
        #self.button.place(x=0, y=self.timer_display_height, width=self.timer_button_width, height=self.timer_button_height)
        self.button.place(relx=0, rely=0.7, relwidth=0.5, relheight=0.3)
        self.button2 = tk.Button(root, text="ストップ", font=("Helvetica",20), state=tk.DISABLED, command=self.stop_timer)
        #self.button2.place(x=self.timer_button_width, y=self.timer_display_height,width=self.timer_button_width, height=self.timer_button_height)
        self.button2.place(relx=0.5, rely=0.7, relwidth=0.5, relheight=0.3)

    def start_timer(self):  #スタートボタン機能
        if self.state_pose:
            self.restart()
        else:
            self.countDown(self.timer*60)
            self.toggle_button_label("counting")

    def stop_timer(self):   #ストップボタン機能
        #タイマーが動いている場合ストップ 
        if self.after_id is not None:
            self.state_pose = True
            self.toggle_button_label("posed")
            self.root.after_cancel(self.after_id)
            self.after_id = None
            self.posed(self.pose_limit*60)
        else:
            self.reset()

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
            self.reset()
        
            
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

    def reset(self):
        self.root.after_cancel(self.pose_id)
        self.toggle_button_label("reset")
        self.state_pose = None
        self.now_count = None
        self.after_id = None
        self.send_notification()
    
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

    def send_notification(self):
        notification.notify(
            title="ポモドーロタイマー",  # 通知のタイトル
            message="25分の集中が終わりました！休憩を取りましょう。",  # 通知の内容
            app_name="Pomodoro Timer",  # アプリ名（任意）
            timeout=10  # 通知が消えるまでの時間（秒）
        )

    

App = app(root)
root.mainloop()