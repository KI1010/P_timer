import pygame
import tkinter as tk

# pygameの初期化
pygame.init()
pygame.mixer.init()

# BGMの設定と再生
pygame.mixer.music.load("notice_sound/BGM1.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # ループ再生

# 効果音の設定
jump_sound = pygame.mixer.Sound('notice_sound/417_BPM110.mp3')
jump_sound.set_volume(0.7)

# 効果音再生
jump_sound.play()

# tkinterウィンドウの作成
root = tk.Tk()
root.title("音声操作アプリ")

# 音声停止の関数
def stop_music():
    pygame.mixer.music.stop()  # BGM停止
    jump_sound.stop()  # 効果音停止

# ボタンの作成
stop_button = tk.Button(root, text="音声停止", command=stop_music)
stop_button.pack(pady=20)

# イベントループ
root.mainloop()

# ゲーム終了時にpygameを終了
pygame.quit()
