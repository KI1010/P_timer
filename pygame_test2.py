import tkinter as tk
import pygame

root = tk.Tk()
root.title("BGMテスト")
root.geometry("500x500")
#音声再生
pygame.init()
pygame.mixer.init()
music1 = "notice_sound/BGM1.mp3"
music2 = "notice_sound/BGM2.mp3"

def music_start1():
    pygame.mixer.music.load(music1)
    pygame.mixer.music.play(start=0.5)

def music_stop():
    pygame.mixer.music.stop()
def music_start2():
    pygame.mixer.music.load(music2)
    pygame.mixer.music.play(start=2)

#UI
label = tk.Label(root, text="test", background="skyblue", font=("Helvetica",15))
label.place(rely=0, relx=0, relwidth=1, relheight=0.2)
button1 = tk.Button(root,text="曲１再生", command=music_start1)
button2 = tk.Button(root,text="停止", command=music_stop)
button3 = tk.Button(root,text="曲２再生", command=music_start2)
button4 = tk.Button(root,text="停止", command=music_stop)
button1.place(rely=0.2, relx=0, relwidth=0.5, relheight=0.2)
button2.place(rely=0.2, relx=0.5, relwidth=0.5, relheight=0.2)
button3.place(rely=0.4, relx=0, relwidth=0.5, relheight=0.2)
button4.place(rely=0.4, relx=0.5, relwidth=0.5, relheight=0.2)

root.mainloop()