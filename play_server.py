# -*- coding: utf-8 -*-
import time
import os
import pygame
import urllib
from io import BytesIO, StringIO

from flask import Flask, render_template, Response, request
from flask import send_from_directory
from flask import url_for

from flask import Flask
app = Flask(__name__)

# Index
@app.route('/')
def index():
    return "Server OK"

# 删除音乐缓存文件
@app.route('/remove', methods=['GET', 'POST'])
def clear():
    # 截取文件名
    filename = request.args.get('file_name')
    print(filename)
    try:
        os.remove(filename)
        return "OK"
    except Exception:
        return "Failed"

# 播放音乐
@app.route('/play', methods=['GET', 'POST'])
def play():
    # 获取URL
    file_url = request.args.get('play_file_name')
    # 截取文件名
    filename = file_url.split('/')[-1]
    
    # 下载音乐文件
    with urllib.request.urlopen(file_url) as web:
        # 为保险起见使用二进制写文件模式，防止编码错误
        try:
            with open(filename, 'wb+') as outfile:
                outfile.write(web.read())
                outfile.close()
        except Exception:
            pass

    # 初始化pygame
    pygame.mixer.init()
    screen=pygame.display.set_mode([640,480])

    #print(f.getvalue())
    # 读入音频文件
    pygame.mixer.music.load(filename)
    # 播放
    pygame.mixer.music.play(0, 0.0)
    print(filename)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')