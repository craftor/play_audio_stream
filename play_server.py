# -*- coding: utf-8 -*-
import time
import os
import pygame
import urllib
from io import BytesIO, StringIO
from waitress import serve


from flask import Flask, render_template, Response, request, redirect
from flask import send_from_directory
from flask import url_for

from flask import Flask
app = Flask(__name__)

from tools import *

# 初始化pygame
pygame.mixer.init()
#screen=pygame.display.set_mode([640,480])

# Index
@app.route('/')
def index():
    # 硬盘情况
    hd_info = disk_status("/")
    # 网络情况
    net_info = net_status()
    # 系统参数
    sys_info = sys_status()
    return render_template("index.html",
                            sys_info=sys_info,
                            hd_info=hd_info,
                            net_info=net_info)

# 检查音乐是否正在播放
@app.route('/get_busy')
def get_busy():
    try:
        result = pygame.mixer.music.get_busy()
        return str(result)
    except Exception:
        return "Failed"

# 停止播放音乐
@app.route('/stop')
def stop():
    try:
        pygame.mixer.music.stop()
        return "OK"
    except Exception:
        return "Failed"

# 暂停
@app.route('/pause')
def pause():
    try:
        pygame.mixer.music.pause()
        return "OK"
    except Exception:
        return "Failed"

# 取消暂停
@app.route('/unpause')
def unpause():
    try:
        pygame.mixer.music.unpause()
        return "OK"
    except Exception:
        return "Failed"

# 设置音量 0.0-1.0
@app.route('/set_volume')
def set_volume():

    try:
        value = float(request.args.get('value'))
        if (value <= 1.0) and (value >= 0.0):
            pass
        else:
            return "Failed"
    except Exception:
        return "Failed"

    try:
        pygame.mixer.music.set_volume(value)
    except Exception:
        return "Failed"

    return "OK"

# 播放序列，每次只能添加一个
@app.route('/queue')
def queue():
    try:
        # 获取URL
        file_url = request.args.get('play_file_name')
        # 截取文件名
        filename = file_url.split('/')[-1]
    except Exception:
        return "Failed"

    # 下载音乐文件
    try:
        with urllib.request.urlopen(file_url) as web:
            # 为保险起见使用二进制写文件模式，防止编码错误
            try:
                with open(filename, 'wb+') as outfile:
                    outfile.write(web.read())
                    outfile.close()
            except Exception:
                pass
    except Exception:
        return "Failed"

    try:
        pygame.mixer.music.queue(filename)
    except Exception:
        return "Failed"

    return "OK"

# 删除音乐缓存文件
@app.route('/remove', methods=['GET', 'POST'])
def clear():
    # 获取文件名
    try:
        filename = request.args.get('play_file_name')
    except Exception:
        return "Failed"
    # 删除文件
    try:
        os.remove(filename)
        return "OK"
    except Exception:
        return "Failed"

# 播放音乐
@app.route('/play', methods=['GET', 'POST'])
def play():

    try:
        # 获取URL
        file_url = request.args.get('play_file_name')
        # 截取文件名
        filename = file_url.split('/')[-1]
    except Exception:
        return "Failed"

    # 获取重复次数
    try:
        loop = int(request.args.get('loop'))
        if (loop < -1):
            return "Failed"
    except Exception:
        loop = 0

    # 获取播放音量
    try:
        volume = float(request.args.get('volume'))
        if (volume <= 1.0) and (volume >= 0.0):
            pass
        else:
            return "Failed"
    except Exception:
        volume = 1.0
    
    # 下载音乐文件
    try:
        with urllib.request.urlopen(file_url) as web:
            # 为保险起见使用二进制写文件模式，防止编码错误
            try:
                with open(filename, 'wb+') as outfile:
                    outfile.write(web.read())
                    outfile.close()
            except Exception:
                pass
    except Exception:
        return "Failed"

    # 读入音频文件
    try:
        pygame.mixer.music.load(filename)
    except Exception:
        return "Failed"

    try:
        # 设置音量
        pygame.mixer.music.set_volume(volume)
    except Exception:
        return "Failed"

    try:
        # 播放
        pygame.mixer.music.play(loop, 0.0)
    except Exception:
        return "Failed"

    return redirect(url_for("index"))

if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=8080)
    app.run(debug=True, host='0.0.0.0',port=8080)
