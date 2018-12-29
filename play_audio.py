
import pygame
import sys
from urllib import request

#http://public.craftor.org/no.wav
#"http://public.craftor.org/bgm.mp3"

url = "http://public.craftor.org/no.wav"
#url = "http://public.craftor.org/bgm.mp3"

filename = url.split('/')[-1]

# with request.urlopen(url) as web:
#     # 为保险起见使用二进制写文件模式，防止编码错误
#     with open('no.wav', 'wb') as outfile:
#         outfile.write(web.read())

#pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode([640,480])
#pygame.time.delay(1000)
pygame.mixer.music.load('bgm.mp3')
pygame.mixer.music.play(0, 0.0)

# while 1:
#     for event in pygame.event.get():
#         if event.type==pygame.QUIT:
#             sys.exit()

# sound = pygame.mixer.Sound('bgm.mp3')
# sound.play()
