import os
import time
import csv
import configparser
import pygame
from datetime import datetime

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import colorchooser

root = tk.Tk()
csv_file = "time_record.csv" #保存するファイルの名前と場所
config_file = "config.ini"

pygame.init()
pygame.mixer.init()

BGM1 = "notice_sound/BGM1.mp3"
BGM2 = "notice_sound/BGM2.mp3"
BGM3 = "notice_sound/BGM3.mp3"
BGM4 = "notice_sound/BGM4.mp3"

class App:
    def __init__(self,root):
        self.root = root
        self.title = root.title("タイマー")
        self.screen_width = self.root.winfo_screenwidth() / 5
        self.screen_height = self.root.winfo_screenheight() * 0.8
        self.geometry = root.geometry(f"{int(self.screen_width)}x{int(self.screen_height)}+0+0")
        #コンフィグ読み込み
        self.config = configparser.ConfigParser()
        self.read_config()
        self.work_time = self.config.getint("User_Setting", "work_time")  #タイマー時間
        self.break_time = self.config.getint("User_Setting", "break_time")  #休憩時間
        self.pose_limit = self.config.getint("User_Setting", "pause_limit_time") #ポーズ中リセットまでのタイムリミット
        self.timer_cycle = self.config.getint("User_Setting", "timer_cycle") #何回タイマーを繰り返すか
        self.message_window_time = self.config.getint("User_Setting", "message_window_time") #メッセージウィンドウの表示時間
        self.default_color = self.config.get("User_Setting", "default_color")
        self.work_color = self.config.get("User_Setting", "work_color")
        self.break_color = self.config.get("User_Setting", "break_color")
        self.cycle_count = None
        self.pose_id = None
        self.root.resizable(False,False)
        self.root.overrideredirect(False)
        self.root.iconbitmap("C:/Users/DCITEX/Desktop/py_ren/pt/P_timer/タイマーアイコン.ico")
        self.state_pose = False
        self.now_count = None
        self.after_id = None
        self.message_window_count_id = None
        self.mute_status = self.config.getboolean("User_Setting", "mute_status") #ミュートかどうか
        self.is_mute = tk.BooleanVar()
        self.is_mute.set(self.mute_status)
        self.loop_status = self.config.get("User_Setting", "is_loop")
        self.is_loop = tk.BooleanVar()
        self.is_loop.set(self.loop_status)
        self.date = None    #タイマー開始時の日付
        self.start_datetime = None  #記録のサイクルのキーに使う
        self.stop_datetime = None 
        self.log_color = None #ログの背景色の判断用
        self.entries = []  #日付の重複確認リスト
        self.selected_color1 = None #色変更用の一時保存のデータ
        self.selected_color2 = None
        self.placed_widgets = []
        self.setting_snapshot = None
        #ウィンドウが閉じるときの動作
        self.root.protocol("WM_DELETE_WINDOW",self.app_end) #保存機能が出来れば、終了時に保存するようにする
        #スタイル
        self.style = ttk.Style()
        self.style.configure("TButton", background="white", font=("Helvetica",20))
        self.style.configure("small.TButton", font=("Helvetica",15))
        self.style.configure("small.TLabel",background="white", font=("Helvetica",12))
        self.style.configure("timer_display.TLabel",background="black",foreground="white",font=("Helvetica",25))
        self.style.configure("log.TFrame", background="skyblue")
        self.style.configure("setting_frame_L.TFrame", background="gray")
        self.style.configure("setting_frame_R.TFrame", background="#ede4e1")
        self.style.configure("setting_notice_tab_header.TLabel", font=("Helvetica",15))
        self.style.configure("setting_notice_tab_radiobutton.TRadiobutton", font=("Helvetica",15), relief="ridge",borderwidth=2)
        self.style.configure("setting_label.TLabel", background="white", font=("Helvetica",15))
        #タイマーウィジェット
        self.timer_frame = ttk.Frame(self.root)
        self.timer_frame.place(relx=0, rely=0,relwidth=1, relheight=0.25)
        self.label = ttk.Label(self.timer_frame, text="タイマー", anchor="center", style="timer_display.TLabel")
        self.label.place(relx=0, rely=0, relwidth=1, relheight=0.7)
        self.button = ttk.Button(self.timer_frame, text="スタート", command=lambda: self.start_timer(), style="TButton")
        self.button.place(relx=0, rely=0.7, relwidth=0.5, relheight=0.3)
        self.button2 = ttk.Button(self.timer_frame, text="ストップ", command=self.stop_timer, state=tk.DISABLED, style="TButton")
        self.button2.place(relx=0.5, rely=0.7, relwidth=0.5, relheight=0.3)
        #ログウィジェット
        self.log_frame= ttk.Frame(self.root, style="log.TFrame")
        self.log_frame.place(relx=0, rely=0.25, relwidth=1, relheight=0.65)
        self.log_list = ttk.Treeview(self.log_frame, columns=("Date", "Start_Time", "Stop_Time"), show="headings")
        self.log_list.heading("Date", text="日付")
        self.log_list.heading("Start_Time", text="開始時刻", anchor="w")
        self.log_list.heading("Stop_Time", text="終了時刻", anchor="w")
        self.log_list.column("Date", width=80, anchor="center")
        self.log_list.column("Start_Time", width=100, anchor="w")
        self.log_list.column("Stop_Time", width=100, anchor="w")
        self.log_list.place(relx=0, rely=0, relwidth=0.9, relheight=1)
        self.scrollbar =  ttk.Scrollbar(self.log_frame, orient="vertical",command=self.log_list.yview)
        self.scrollbar.place(relx=0.9, rely=0, relwidth=0.1, relheight=1)
        self.log_list.config(yscrollcommand=self.scrollbar.set)
        self.log_list.bind("<Button-1>", self.disable_resize)
        self.log_list.bind("<B1-Motion>", self.disable_resize)
        self.log_list.tag_configure("Default_Color", background=self.default_color)
        self.log_list.tag_configure("Work", background=self.work_color)
        self.log_list.tag_configure("Break", background=self.break_color)
        #フッターウィジェット
        self.footer_frame = ttk.Frame(self.root)
        self.footer_frame.place(relx=0, rely=0.9, relwidth=1, relheight=0.1)
        self.exit_button = ttk.Button(self.footer_frame, text="Exit", command=self.app_end, style="TButton")
        self.exit_button.place(relx=0, rely=0, relwidth=0.75, relheight=1)
        self.setting_button = ttk.Button(self.footer_frame, text="設定", style="TButton", command=self.call_setting_window)
        self.setting_button.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)
        #子ウィンドウ
        self.message_window = None
        self.setting_window = None
        self.work_time_color_before_sample = None
        self.break_time_color_before_sample = None
        #過去ログ読み込み
        self.read_csv()

    def read_config(self): #コンフィグファイルを読み込む
        if not os.path.exists(config_file):
            print("ファイルがないです")
            return
        try:
            with open(config_file, encoding="UTF-8") as f:
                self.config.read_file(f)
        except FileNotFoundError:
            print("ファイルがありません")
        except UnicodeDecodeError as e:
            print(f"UnicodeDecodeError: {e}. ファイルのエンコーディングを確認してください。")

    def start_timer(self):  #スタートボタン機能
        if self.state_pose:
            self.restart()
        else:
            if self.cycle_count is None:
                self.cycle_count = self.timer_cycle

            timer_duration = self.get_duration()

            self.countDown(timer_duration)
            self.toggle_button_label("counting")
            self.start_datetime = self.get_current_time()
            self.date = self.get_current_date()

    def get_duration(self): #作業時間か休憩時間かを判断して
        if self.cycle_count % 2 == 0:
            self.log_color = "Work"
            return self.work_time * 60
        else:
            self.log_color = "Break"
            return self.break_time * 60

    def stop_timer(self):   #ストップボタン機能
        if self.after_id is not None:
            self.state_pose = True
            self.toggle_button_label("posed")
            self.root.after_cancel(self.after_id)
            self.after_id = None
            self.posed(self.pose_limit*60)
            self.stop_datetime = self.get_current_time()
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
        if total_seconds > 0: #タイマーカウントの処理
            mins,secs = divmod(total_seconds,60)
            timer = f"{mins:02}:{secs:02}"
            self.label["text"] = timer
            self.now_count = total_seconds
            self.after_id = self.root.after(1000,self.countDown,total_seconds -1)
        else: #タイマー終了時の処理
            self.toggle_button_label("complete")
            self.cycle_count -= 1
            self.stop_datetime = self.get_current_time()
            self.data_loading(self.date,self.start_datetime,self.stop_datetime,self.log_color)
            self.record_save()
            if self.cycle_count == 0:
                self.toggle_button_label("reset")
                self.cycle_count = None
                print("1サイクル終了しました")
            else:
                self.send_message()

    def reset(self):
        if self.state_pose: #ポーズ中の場合 
            self.root.after_cancel(self.pose_id)
            self.state_pose = False
            self.now_count = None
            self.after_id = None
            self.data_loading(self.date,self.start_datetime,self.stop_datetime,self.log_color)
            self.record_save()
            self.date = None
            self.start_datetime = None
            self.stop_datetime = None
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
        self.message_window.protocol("WM_DELETE_WINDOW",self.stop_timer_cycle) #ウィンドウ削除時の処理
        self.check_mute_status()
        #BGMのループ分岐を入れる
        loop = self.is_loop.get()
        if loop:
            #Trueなら自分で止めるまで動くように
            loop_message_label1 = ttk.Label(self.message_window, text="時間になりました")
            loop_message_label2 = ttk.Label(self.message_window, text="次のタイマーを実行するか選択してください")
            loop_message_buton1 = ttk.Button(self.message_window, text="タイマー停止", command=lambda :self.stop_timer_cycle())
            loop_message_buton2 = ttk.Button(self.message_window, text="タイマー実行", command=self.start_next_timer)
            
            loop_message_label1.pack()
            loop_message_label2.pack()
            loop_message_buton1.pack()
            loop_message_buton2.pack()
        else:
            count_message_label1 = ttk.Label(self.message_window, text="5秒後にタイマーが開始します")
            count_message_label2 = ttk.Label(self.message_window, text="ボタンを押すと停止します")
            count_message_buton1 = ttk.Button(self.message_window,text="停止",command=lambda :self.stop_timer_cycle())

            count_message_label1.pack()
            count_message_label2.pack()
            count_message_buton1.pack()
            self.start_next_timer_count(self.message_window_time,count_message_label1)

    def stop_timer_cycle(self):  #メッセージウィンドウを消し、カウントダウンを止める
        if self.is_loop.get() is False:
            self.root.after_cancel(self.message_window_count_id)    #メッセージウィンドウのカウントを止める
        self.message_window.destroy()                               #メッセージウィンドウを消す
        pygame.mixer.music.stop()                                   #音声再生を止める
        self.reset()

    def start_next_timer_count(self,count,label):
        if count > 0:
            label["text"] = f"{count}秒後にタイマーが開始します"
            self.message_window_count_id = self.root.after(1000,self.start_next_timer_count,count -1,label)
        else:
            self.start_next_timer()
    
    def start_next_timer(self):
        pygame.mixer.music.stop()  #音声再生を止める
        self.message_window.destroy()
        self.toggle_button_label("counting")
        self.start_timer()
    #設定ウィンドウ
    def call_setting_window(self):
        if self.setting_window is None or not self.setting_window.winfo_exists():
            self.create_setting_window()
        else:
            self.setting_window.deiconify()
            self.setting_window.lift()
            self.setting_window.focus_force()

    def create_setting_window(self): #設定ウィンドウ作成　タブ作成
        self.setting_window = tk.Toplevel(root)
        self.setting_window.title("設定")
        self.setting_window.geometry("500x300+0+0")

        setting_frame_L = ttk.Frame(self.setting_window, style="setting_frame_L.TFrame") #カテゴリ
        setting_frame_R = ttk.Frame(self.setting_window, style="setting_frame_R.TFrame") #詳細欄
        setting_frame_L.place(relx=0, rely=0, relwidth=0.3, relheight=1)
        setting_frame_R.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)
        #タブ選択ボタン
        setting_button1 = ttk.Button(setting_frame_L, text="通知設定", style="TButton", command=lambda : self.place_notice_tab(setting_frame_R))
        setting_button2 = ttk.Button(setting_frame_L, text="時間設定", style="TButton", command=lambda : self.place_pomodoro_tab(setting_frame_R))
        setting_button3 = ttk.Button(setting_frame_L, text="表示設定", style="TButton", command=lambda : self.place_display_tab(setting_frame_R))
        setting_button4 = ttk.Button(setting_frame_L, text="リセット", style="TButton", command=lambda : self.place_reset_tab(setting_frame_R))
        setting_button1.place(relx=0, rely=0,   relwidth=1, relheight=0.2)
        setting_button2.place(relx=0, rely=0.2, relwidth=1, relheight=0.2)
        setting_button3.place(relx=0, rely=0.4, relwidth=1, relheight=0.2)
        setting_button4.place(relx=0, rely=0.6, relwidth=1, relheight=0.2)
        #初期表示
        self.get_setting_snapshot()
        self.place_notice_tab(setting_frame_R)
        #ウィンドウを一つのみにするための設定
        self.setting_window.protocol("WM_DELETE_WINDOW", self.setting_window_close)
        #タイマー時間の設定

    def place_notice_tab(self,setting_frame_R): #通知機能のタブを生成
        self.check_changed()
        self.delete_tab()
        mute_setting_label = ttk.Label(setting_frame_R, text="通知音の有無を選択してください", style="setting_notice_tab_header.TLabel")
        mute_radio1 = ttk.Radiobutton(setting_frame_R,
                                      variable=self.is_mute,
                                      style="setting_notice_tab_radiobutton.TRadiobutton",
                                      text="通知音なし",
                                      value=True,
                                      command=lambda:self.config.set("User_Setting","mute_status","True"))
        mute_radio2 = ttk.Radiobutton(setting_frame_R,
                                      variable=self.is_mute,
                                      style="setting_notice_tab_radiobutton.TRadiobutton",
                                      text="通知音あり",
                                      value=False,
                                      command=lambda:self.config.set("User_Setting","mute_status","False"))
        display_time_label_left = ttk.Label(setting_frame_R, text="次にタイマーまでの時間", style="setting_notice_tab_header.TLabel")
        display_time_label_center = ttk.Label(setting_frame_R, text=self.message_window_time, style="setting_notice_tab_header.TLabel")
        display_time_label_right = ttk.Label(setting_frame_R, text="秒", style="setting_notice_tab_header.TLabel")
        display_time_scale = ttk.Scale(setting_frame_R,
                                       from_=0,
                                       to=10,
                                       orient="horizontal",
                                       command=lambda event=None : self.change_scale(display_time_label_center, display_time_scale, "User_Setting", "message_window_time"))
        display_time_scale.set(str(self.message_window_time))
        loop_setting_label = ttk.Label(setting_frame_R, text="次のタイマーを自動開始")
        loop_radio1 = ttk.Radiobutton(setting_frame_R,
                                      variable=self.is_loop,
                                      style="setting_notice_tab_radiobutton.TRadiobutton",
                                      text="ON",
                                      value=False,
                                      command=lambda:self.config.set("User_Setting","is_loop","False"))
        loop_radio2 = ttk.Radiobutton(setting_frame_R,
                                      variable=self.is_loop,
                                      style="setting_notice_tab_radiobutton.TRadiobutton",
                                      text="OFF",
                                      value=True,
                                      command=lambda:self.config.set("User_Setting","is_loop","True"))


        mute_setting_label.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        mute_radio1.place(relx=0, rely=0.1, relwidth=0.5, relheight=0.2)
        mute_radio2.place(relx=0.5, rely=0.1, relwidth=0.5, relheight=0.2)
        display_time_label_left.place(relx=0, rely=0.3, relwidth=0.7, relheight=0.1)
        display_time_label_center.place(relx=0.7, rely=0.3, relwidth=0.2, relheight=0.1)
        display_time_label_right.place(relx=0.9, rely=0.3, relwidth=0.1, relheight=0.1)
        display_time_scale.place(relx=0, rely=0.4, relwidth=1, relheight=0.1)
        loop_setting_label.place(relx=0, rely=0.5, relwidth=1, relheight=0.1)
        loop_radio1.place(relx=0, rely=0.6, relwidth=0.5, relheight=0.2)
        loop_radio2.place(relx=0.5, rely=0.6, relwidth=0.5, relheight=0.2)

        self.placed_widgets.append(mute_setting_label)
        self.placed_widgets.append(mute_radio1)
        self.placed_widgets.append(mute_radio2)
        self.placed_widgets.append(display_time_label_left)
        self.placed_widgets.append(display_time_label_center)
        self.placed_widgets.append(display_time_label_right)
        self.placed_widgets.append(display_time_scale)
        self.placed_widgets.append(loop_setting_label)
        self.placed_widgets.append(loop_radio1)
        self.placed_widgets.append(loop_radio2)
        self.place_setting_button(setting_frame_R)

    def place_pomodoro_tab(self,setting_frame_R): #タイマーに関する設定タブを生成
        self.check_changed()
        self.delete_tab()
        #サイクル
        cycle_label_left = ttk.Label(setting_frame_R, text="サイクル", style="setting_label.TLabel")
        cycle_label_center = ttk.Label(setting_frame_R, text=self.timer_cycle, style="setting_label.TLabel")
        cycle_label_right = ttk.Label(setting_frame_R, text="回", style="setting_label.TLabel")
        cycle_scale = ttk.Scale(setting_frame_R,
                                from_=1, to=20,
                                orient="horizontal",
                                command=lambda event=None : self.change_scale(cycle_label_center, cycle_scale, "User_Setting", "timer_cycle"))
        cycle_scale.set(str(self.timer_cycle))
        cycle_label_left.place(relx=0, rely=0, relwidth=0.7, relheight=0.1)
        cycle_label_center.place(relx=0.7, rely=0, relwidth=0.2, relheight=0.1)
        cycle_label_right.place(relx=0.9, rely=0, relwidth=0.1, relheight=0.1)
        cycle_scale.place(relx=0, rely=0.1, relwidth=1, relheight=0.1)
        #作業時間
        work_time_label_left = ttk.Label(setting_frame_R, text="作業時間", style="setting_label.TLabel")
        work_time_label_center = ttk.Label(setting_frame_R, text=self.work_time, style="setting_label.TLabel")
        work_time_label_right = ttk.Label(setting_frame_R, text="分", style="setting_label.TLabel")
        work_time_scale = ttk.Scale(setting_frame_R,
                                    from_=1,
                                    to=60,
                                    orient="horizontal",
                                    command=lambda event=None : self.change_scale(work_time_label_center, work_time_scale, "User_Setting", "work_time"))
        work_time_scale.set(self.work_time)
        work_time_label_left.place(relx=0, rely=0.2, relwidth=0.7, relheight=0.1)
        work_time_label_center.place(relx=0.7, rely=0.2, relwidth=0.2, relheight=0.1)
        work_time_label_right.place(relx=0.9, rely=0.2, relwidth=0.1, relheight=0.1)
        work_time_scale.place(relx=0, rely=0.3, relwidth=1, relheight=0.1)
        #休憩時間
        break_time_label_left = ttk.Label(setting_frame_R, text="休憩時間", style="setting_label.TLabel")
        break_time_label_center = ttk.Label(setting_frame_R, text=self.break_time, style="setting_label.TLabel")
        break_time_label_right = ttk.Label(setting_frame_R, text="分", style="setting_label.TLabel")
        break_time_scale = ttk.Scale(setting_frame_R,
                                     from_=1,
                                     to=30,
                                     orient="horizontal",
                                     command=lambda event=None : self.change_scale(break_time_label_center, break_time_scale, "User_Setting", "break_time"))
        break_time_scale.set(self.break_time)
        break_time_label_left.place(relx=0, rely=0.4, relwidth=0.7, relheight=0.1)
        break_time_label_center.place(relx=0.7, rely=0.4, relwidth=0.2, relheight=0.1)
        break_time_label_right.place(relx=0.9, rely=0.4, relwidth=0.1, relheight=0.1)
        break_time_scale.place(relx=0, rely=0.5, relwidth=1, relheight=0.1)

        self.placed_widgets.append(cycle_label_left)
        self.placed_widgets.append(cycle_label_center)
        self.placed_widgets.append(cycle_label_right)
        self.placed_widgets.append(cycle_scale)
        self.placed_widgets.append(work_time_label_left)
        self.placed_widgets.append(work_time_label_center)
        self.placed_widgets.append(work_time_label_right)
        self.placed_widgets.append(work_time_scale)
        self.placed_widgets.append(break_time_label_left)
        self.placed_widgets.append(break_time_label_center)
        self.placed_widgets.append(break_time_label_right)
        self.placed_widgets.append(break_time_scale)
        self.place_setting_button(setting_frame_R)

    def place_display_tab(self,setting_frame_R): #表示設定のタブを生成
        self.check_changed()
        self.delete_tab()
        work_time_color_label = ttk.Label(setting_frame_R, text="作業時間の背景色", style="setting_label.TLabel")
        self.work_time_color_before_sample = ttk.Label(setting_frame_R, borderwidth=5, relief="solid", text="今の色", anchor="center")
        work_time_color_after_sample = ttk.Label(setting_frame_R, borderwidth=5, relief="solid", text="新しい色", anchor="center")

        break_time_color_label = ttk.Label(setting_frame_R, text="休憩時間の背景色", style="setting_label.TLabel")
        self.break_time_color_before_sample = ttk.Label(setting_frame_R, borderwidth=5, relief="solid", text="今の色", anchor="center")
        break_time_color_after_sample = ttk.Label(setting_frame_R, borderwidth=5, relief="solid", text="新しい色", anchor="center")

        work_color_selection_button = ttk.Button(setting_frame_R, text="作業時間の\n色を選択", style="small.TButton", command=lambda : self.selecting_color(work_time_color_after_sample, "work"))
        break_color_selection_button = ttk.Button(setting_frame_R, text="休憩時間の\n色を選択", style="small.TButton", command=lambda : self.selecting_color(break_time_color_after_sample, "break"))

        self.work_time_color_before_sample.config(background=self.work_color) #今適応されている色に設定
        self.break_time_color_before_sample.config(background=self.break_color)

        work_time_color_label.place(relx=0, rely=0, relwidth=0.6, relheight=0.2)
        self.work_time_color_before_sample.place(relx=0.6, rely=0, relwidth=0.2, relheight=0.2)
        work_time_color_after_sample.place(relx=0.8, rely=0, relwidth=0.2, relheight=0.2)
        break_time_color_label.place(relx=0, rely=0.2, relwidth=0.6, relheight=0.2)
        self.break_time_color_before_sample.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.2)
        break_time_color_after_sample.place(relx=0.8, rely=0.2, relwidth=0.2, relheight=0.2)
        work_color_selection_button.place(relx=0, rely=0.4, relwidth=0.5, relheight=0.2)
        break_color_selection_button.place(relx=0.5, rely=0.4, relwidth=0.5, relheight=0.2)

        self.placed_widgets.append(work_time_color_label)
        self.placed_widgets.append(self.work_time_color_before_sample)
        self.placed_widgets.append(work_time_color_after_sample)
        self.placed_widgets.append(break_time_color_label)
        self.placed_widgets.append(self.break_time_color_before_sample)
        self.placed_widgets.append(break_time_color_after_sample)
        self.placed_widgets.append(work_color_selection_button)
        self.placed_widgets.append(break_color_selection_button)
        self.place_setting_button(setting_frame_R)

    def place_reset_tab(self,setting_flame_R): #リセット機能のタブを生成
        self.check_changed()
        self.delete_tab()
        reset_label1 = ttk.Label(setting_flame_R, style="small.TLabel", text="通知ウィンドウの表示時間")
        reset_label2 = ttk.Label(setting_flame_R, style="small.TLabel", text="サイクル")
        reset_label3 = ttk.Label(setting_flame_R, style="small.TLabel", text="作業時間")
        reset_label4 = ttk.Label(setting_flame_R, style="small.TLabel", text="休憩時間")
        reset_label5 = ttk.Label(setting_flame_R, style="small.TLabel", text="作業時間背景色")
        reset_label6 = ttk.Label(setting_flame_R, style="small.TLabel", text="休憩時間背景色")

        reset_button1 = ttk.Button(setting_flame_R, text="リセット", style="small.TButton", command=lambda : self.setting_reset("message_window_time"))
        reset_button2 = ttk.Button(setting_flame_R, text="リセット", style="small.TButton", command=lambda : self.setting_reset("timer_cycle"))
        reset_button3 = ttk.Button(setting_flame_R, text="リセット", style="small.TButton", command=lambda : self.setting_reset("work_time"))
        reset_button4 = ttk.Button(setting_flame_R, text="リセット", style="small.TButton", command=lambda : self.setting_reset("break_time"))
        reset_button5 = ttk.Button(setting_flame_R, text="リセット", style="small.TButton", command=lambda : self.setting_reset("work_color"))
        reset_button6 = ttk.Button(setting_flame_R, text="リセット", style="small.TButton", command=lambda : self.setting_reset("break_color"))

        reset_label1.place(relx=0, rely=0,    relwidth=0.7, relheight=0.15)
        reset_label2.place(relx=0, rely=0.15, relwidth=0.7, relheight=0.15)
        reset_label3.place(relx=0, rely=0.3,  relwidth=0.7, relheight=0.15)
        reset_label4.place(relx=0, rely=0.45, relwidth=0.7, relheight=0.15)
        reset_label5.place(relx=0, rely=0.6,  relwidth=0.7, relheight=0.15)
        reset_label6.place(relx=0, rely=0.75, relwidth=0.7, relheight=0.15)

        reset_button1.place(relx=0.7, rely=0,    relwidth=0.3, relheight=0.15)
        reset_button2.place(relx=0.7, rely=0.15, relwidth=0.3, relheight=0.15)
        reset_button3.place(relx=0.7, rely=0.3,  relwidth=0.3, relheight=0.15)
        reset_button4.place(relx=0.7, rely=0.45, relwidth=0.3, relheight=0.15)
        reset_button5.place(relx=0.7, rely=0.6,  relwidth=0.3, relheight=0.15)
        reset_button6.place(relx=0.7, rely=0.75, relwidth=0.3, relheight=0.15)

        self.placed_widgets.append(reset_label1)
        self.placed_widgets.append(reset_label2)
        self.placed_widgets.append(reset_label3)
        self.placed_widgets.append(reset_label4)
        self.placed_widgets.append(reset_label5)
        self.placed_widgets.append(reset_label6)
        self.placed_widgets.append(reset_button1)
        self.placed_widgets.append(reset_button2)
        self.placed_widgets.append(reset_button3)
        self.placed_widgets.append(reset_button4)
        self.placed_widgets.append(reset_button5)
        self.placed_widgets.append(reset_button6)

    def setting_reset(self, target): #設定をデフォルトに戻す
        default_data = self.config.get("DEFAULT",target)
        print(target +":"+ default_data)
        self.config.set("User_Setting", target, default_data)
        self.setting_save()

    def selecting_color(self, preview, current_mode): #カラーパレットから色を選びプレビューに反映
        color_code = colorchooser.askcolor(title="色を選択してください")
        if color_code[1]:
            if current_mode == "work":
                self.selected_color1 = color_code[1]
                preview.config(background=self.selected_color1)
                self.config.set("User_Setting", "work_color", self.selected_color1)
            elif current_mode == "break":
                self.selected_color2 = color_code[1]
                preview.config(background=self.selected_color2)
                self.config.set("User_Setting", "break_color", self.selected_color2)
            else:
                print("current_modeの値が不正です")
        else:
            print("色の変更をキャンセルしました")
        self.setting_window.lift() #設定ウィンドウが後ろに行くのを防ぐ

    def apply_tag_color(self): #色の変更を反映
        self.log_list.tag_configure("Work", background=self.work_color)
        self.log_list.tag_configure("Break", background=self.break_color)
        if self.work_time_color_before_sample != None:
            self.work_time_color_before_sample.config(background=self.work_color)
            self.break_time_color_before_sample.config(background=self.break_color)

    def change_scale(self, label, scale, section, key): #スケールの変更を反映
        label.config(text=int(scale.get()))
        self.config.set(section, key, f"{int(scale.get())}")

    def place_setting_button(self,frame): #設定保存ボタン機能
        save_button = ttk.Button(frame, text="設定を保存", style="TButton", command=self.setting_save)
        save_button.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)
        self.placed_widgets.append(save_button) #設置ウィジェットリストに追加

    def setting_save(self): #変更した設定を保存する
        with open(config_file, "w") as f:
            self.config.write(f)
        self.apply_setting()
        self.apply_tag_color()
        self.get_setting_snapshot()

    def delete_tab(self): #タブを削除
        for w in self.placed_widgets:
            w.place_forget()

    def setting_window_close(self):
        self.setting_window.destroy()
        self.apply_setting()
        self.setting_window = None
        self.placed_widgets = []
        self.setting_snapshot = None

    def get_setting_snapshot(self): #設定変更時に保存
        self.setting_snapshot = {
            "work_time":self.config.getint("User_Setting", "work_time"),
            "break_time":self.config.getint("User_Setting", "break_time"),
            "pause_limit_time":self.config.getint("User_Setting", "pause_limit_time"),
            "timer_cycle":self.config.getint("User_Setting", "timer_cycle"),
            "message_window_time":self.config.getint("User_Setting", "message_window_time"),
            "mute_status":self.config.getboolean("User_Setting", "mute_status"),
            "default_color":self.config.get("User_Setting", "default_color"),
            "work_color":self.config.get("User_Setting", "work_color"),
            "break_color":self.config.get("User_Setting", "break_color"),
            "is_loop":self.config.get("User_Setting", "is_loop")
        }

    def rollback_to_snapshot(self): #スナップショットを利用してロールバックする
        for key , value in self.setting_snapshot.items():
            self.config.set("User_Setting", key, str(value))
        self.is_mute.set(self.mute_status)
        self.is_loop.set(self.loop_status)

    def load_config(self): #今の設定からデータを取得
        return[
            self.config.getint("User_Setting", "work_time"),
            self.config.getint("User_Setting", "break_time"),
            self.config.getint("User_Setting", "pause_limit_time"),
            self.config.getint("User_Setting", "timer_cycle"),
            self.config.getint("User_Setting", "message_window_time"),
            self.config.getboolean("User_Setting", "mute_status"),
            self.config.get("User_Setting", "default_color"),
            self.config.get("User_Setting", "work_color"),
            self.config.get("User_Setting", "break_color"),
            self.config.get("User_Setting", "is_loop")
        ]
    
    def check_changed(self): #設定未変更を検知
        snapshot_list = list(self.setting_snapshot.values())
        current_setting_data = self.load_config()
        if snapshot_list == current_setting_data:
            print("変更はありません")
        else:
            result = messagebox.askyesno("確認", "保存していない設定があります\n設定を保存しますか", parent=self.setting_window)
            if result: #設定を保存し　スナップショットを更新する
                self.setting_save()
            else:
                self.rollback_to_snapshot()

    def apply_setting(self): #設定ファイルから再読み込み
        self.work_time = self.config.getint("User_Setting", "work_time")
        self.break_time = self.config.getint("User_Setting", "break_time")  #休憩時間
        self.pose_limit = self.config.getint("User_Setting", "pause_limit_time") #ポーズ中リセットまでのタイムリミット
        self.timer_cycle = self.config.getint("User_Setting", "timer_cycle") #何回タイマーを繰り返すか
        self.message_window_time = self.config.getint("User_Setting", "message_window_time")
        self.mute_status = self.config.getboolean("User_Setting", "mute_status") #ミュートかどうか
        self.is_mute.set(self.mute_status)
        self.default_color = self.config.get("User_Setting", "default_color")
        self.work_color = self.config.get("User_Setting", "work_color")
        self.break_color = self.config.get("User_Setting", "break_color")
        self.loop_status = self.config.get("User_Setting", "is_loop")
        self.is_loop.set(self.loop_status)

    def check_mute_status(self): #通知音を判別
        mute = self.is_mute.get()
        if mute:
            print("時間です--Mute ON--")
        else:
            print("時間です--MUte OFF")
            self.play_sound_notice()

    def play_sound_notice(self): #音楽を再生
        #通知音のが音楽かシンプルかの判定を入れる
        pygame.mixer.music.load(BGM4)
        loop = self.is_loop.get()
        if loop:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.play()

    def get_current_time(self): #現在時刻を所得して返す機能
        current_time = datetime.now()
        format_time = current_time.strftime("%H:%M:%S")
        return format_time
    
    def get_current_date(self): #日付を取得して返す機能
        current_date = datetime.now()
        format_date = current_date.strftime("%Y-%m-%d")
        return format_date
    
    def is_valid_date(self,date_string): #日付のチェック
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
        
    def is_valid_time(self,time_string):
        try:
            datetime.strptime(time_string, "%H:%M:%S")
            return True
        except ValueError:
            return False
        
    def is_valid_date_time(self):
        if not self.is_valid_date(self.date):
            print(f"日付データの形式が不正です:{self.date}")
            return False
        if not self.is_valid_time(self.start_datetime):
            print(f"タイマー開始時刻の形式が不正です:{self.start_datetime}")
            return False
        if not self.is_valid_time(self.stop_datetime):
            print(f"タイマー終了時刻の形式が不正です:{self.stop_datetime}")
            return False
        return True
    
    def record_save(self): #CSVファイルに保存
        if not self.is_valid_date_time(): #形式チェックを入れる
            return
        
        with open(csv_file, "a", newline="") as file :
            writer = csv.writer(file)
            file.seek(0, 2) #ファイルの最後尾に入力位置を移動する
            if file.tell() == 0:    #何もデータが無ければリストの名前を最初に入力する
                writer.writerow(["日付","開始時間","終了時間"])

            writer.writerow([self.date,self.start_datetime,self.stop_datetime,self.log_color])
        self.date = None
        self.start_datetime = None
        self.stop_datetime = None
        self.log_color = None

    def read_csv(self): #csvデータを読み込み
        if not os.path.exists(csv_file):
            print(f"ファイル{csv_file}が存在しません")
            return
        
        try:
            with open(csv_file, mode="r") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    value3 = row[3] if len(row) > 3 else "Default_Color"
                    self.data_loading(row[0], row[1], row[2], value3)
        except Exception as e:
            print(f"エラーが発生しました：{e}")
        self.log_list.yview_moveto(1) #初期位置を下に

    def data_loading(self,date,start,stop,tag): #ログの最後にデータを追加
        date_obj =  datetime.strptime(date, "%Y-%m-%d").date()
        date = date_obj.strftime("%Y-%m-%d")

        same_date_entries = [entry for entry in self.entries if entry[0] == date]

        if len(same_date_entries) == 0:
            self.log_list.insert("", "end", values=(date, start, stop), tags=(tag,))
        else:
            self.log_list.insert("", "end", values=("", start, stop), tags=(tag,))

        self.entries.append((date, self.log_list.get_children()[-1] if self.log_list.get_children() else None))

    def disable_resize(self,event):
        return "break"
    
    def app_end(self):#アプリを終了する
        if self.date is not None: #日付データがある場合
            if self.state_pose is False: 
                self.stop_datetime = self.get_current_time()
            self.record_save()
        root.destroy()

App = App(root)
root.mainloop()