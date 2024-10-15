import tkinter as tk
import time
from tkinter import messagebox

root = tk.Tk()

class app:
    def __init__(self,root):
        self.root = root
        self.title = root.title("タイマー")
        self.screen_width = self.root.winfo_screenwidth() / 5
        self.screen_height = self.root.winfo_screenheight() * 0.8
        self.geometry = root.geometry(f"{int(self.screen_width)}x{int(self.screen_height)}+0+0")
        self.timer = 0.1  #タイマー時間
        self.timer2 = 1  #休憩時間
        self.pose_limit = 1 #ポーズ中リセットまでのタイムリミット
        self.timer_cycle = 6 #何回タイマーを繰り返すか
        self.message_window_time = 5 #メッセージウィンドウの表示時間
        self.cycle_count = None
        self.pose_id = None
        self.root.resizable(False,False)
        self.root.overrideredirect(False)
        self.root.iconbitmap("C:/Users/DCITEX/Desktop/py_ren/pt/P_timer/タイマーアイコン.ico")
        self.state_pose = False
        self.now_count = None
        self.after_id = None
        self.message_window_count_id = None
        self.selected_value = None#初期値を後で設定する　通知方法の選択に使う

        #ウィジェット
        #タイマー
        self.timer_frame = tk.Frame(root)
        self.timer_frame.place(relx=0, rely=0,relwidth=1, relheight=0.25)
        self.label = tk.Label(self.timer_frame, text="タイマー", bg="black", fg="white", font=("Helvetica",25))
        self.label.place(relx=0, rely=0, relwidth=1, relheight=0.7)
        self.button = tk.Button(self.timer_frame, text="スタート", command=lambda: self.start_timer(), font=("Helvetica",20))
        self.button.place(relx=0, rely=0.7, relwidth=0.5, relheight=0.3)
        self.button2 = tk.Button(self.timer_frame, text="ストップ", font=("Helvetica",20), state=tk.DISABLED, command=self.stop_timer)
        self.button2.place(relx=0.5, rely=0.7, relwidth=0.5, relheight=0.3)
        #ログ
        self.log_frame= tk.Frame(root,bg="skyblue")
        self.log_frame.place(relx=0, rely=0.25, relwidth=1, relheight=0.65)
        #フッター
        self.footer_frame = tk.Frame(root)
        self.footer_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
        self.exit_button = tk.Button(self.footer_frame, text="Exit", font=("Helvetica",20), command=self.app_end)
        self.exit_button.place(relx=0, rely=0, relwidth=0.75, relheight=1)
        self.setting_button = tk.Button(self.footer_frame, text="設定", font=("Helvetica",20), command=self.call_setting_window)
        self.setting_button.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)
        #子ウィンドウ
        self.message_window = None
        self.setting_window = None

    def start_timer(self):  #スタートボタン機能
        if self.state_pose:
            self.restart()
        else:
            while True:
                if  self.cycle_count is not None:
                    if self.cycle_count % 2 == 0:
                        self.countDown(self.timer * 60)
                        self.toggle_button_label("counting")
                        break
                    else:
                        self.countDown(self.timer2 * 60)
                        self.toggle_button_label("counting")
                        break
                else:
                    self.cycle_count = self.timer_cycle

    def stop_timer(self):   #ストップボタン機能
        if self.after_id is not None:
            self.state_pose = True
            self.toggle_button_label("posed")
            self.root.after_cancel(self.after_id)
            self.after_id = None
            self.posed(self.pose_limit*60)
        else:
            self.reset()

    def posed(self,pose_count): #一時停止の処理
        if pose_count > 0:      #点滅機能
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
           
    def countDown(self,total_seconds): #カウントダウン機能
        if total_seconds > 0:
            mins,secs = divmod(total_seconds,60)
            timer = f"{mins:02}:{secs:02}"
            self.label["text"] = timer
            self.now_count = total_seconds
            self.after_id = self.root.after(1000,self.countDown,total_seconds -1)
        else:
            self.toggle_button_label("complete")
            self.cycle_count -= 1
            if self.cycle_count == 0:
                self.toggle_button_label("reset")
                self.cycle_count = None
            else:
                self.send_message()

    def reset(self):
        if self.state_pose: #ポーズ中の場合
            self.root.after_cancel(self.pose_id)
            self.state_pose = False
            self.now_count = None
            self.after_id = None
        self.toggle_button_label("reset")
        self.cycle_count = None
    
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
            case "complete":
                self.label["text"] = "タイマー終了"
                self.button["text"] = "スタート"
                self.button2["text"] = "ストップ"
                self.button.config(state=tk.DISABLED)
                self.button2.config(state=tk.DISABLED)
    #確認ウィンドウ           
    def send_message(self):
        self.message_window = tk.Toplevel(root)
        self.message_window.title("確認")
        message_label = tk.Label(self.message_window, text="5秒後にタイマーが開始します")
        message_label2 = tk.Label(self.message_window, text="ボタンを押すと停止します")
        message_buton = tk.Button(self.message_window,text="停止",command=lambda :self.stop_timer_cycle())

        message_label.pack()
        message_label2.pack()
        message_buton.pack()
        self.start_next_timer_count(self.message_window_time,message_label)

    def stop_timer_cycle(self):  #メッセージウィンドウを消し、カウントダウンを止める
        self.message_window.destroy()                           #メッセージウィンドウを消す
        self.root.after_cancel(self.message_window_count_id)    #メッセージウィンドウのカウントを止める
        self.reset()

    def start_next_timer_count(self,count,label):
        if count > 0:
            label["text"] = f"{count}秒後にタイマーが開始します"
            self.message_window_count_id = self.root.after(1000,self.start_next_timer_count,count -1,label)
        else:
            self.message_window.destroy()
            self.toggle_button_label("counting")
            self.start_timer()
    #設定ウィンドウ
    def call_setting_window(self):
        self.setting_window = tk.Toplevel(root)
        self.setting_window.title("設定")
        self.setting_window.geometry("500x300+0+0")

        setting_frame_L = tk.Frame(self.setting_window,bg="gray") #分類
        setting_frame_L.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        setting_frame_R = tk.Frame(self.setting_window,bg="#ede4e1") #詳細
        setting_frame_R.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

        setting_button1 = tk.Button(setting_frame_L, text="通知方法", font=("Helvetica",20))
        setting_button1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
        #通知の設定
        setting_label1 = tk.Label(setting_frame_R, text="通知方法を選択してください", font=("Helvetica",15))
        setting_label1.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        radio1 = tk.Radiobutton(setting_frame_R, font=("Helvetica",15),relief="ridge" , text="通知のみ", variable=self.selected_value, value=1)
        radio2 = tk.Radiobutton(setting_frame_R, font=("Helvetica",15),relief="ridge" , text="通知音あり", variable=self.selected_value, value=2)
        radio1.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.2)
        radio2.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.2)


    def app_end(self):#アプリを終了する
        root.destroy()
    

App = app(root)
root.mainloop()