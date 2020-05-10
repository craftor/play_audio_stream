# -*- coding: UTF8 -*-

import os, sys
import json
import time
import datetime
import netifaces
import re
import psutil


'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''
def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)


'''获取文件的修改时间'''
def get_FileModifyTime(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)


def disk_status(folder):
    """
    查看文件夹占用磁盘信息
    :param folder: 文件夹路径
    :return:
    """
    hd={}
    disk = os.statvfs(folder)
    # print(disk)
    # 剩余
    free = disk.f_bavail * disk.f_frsize
    hd['free'] = str(round(free/float(1024*1024*1024), 2)) + " GB"
    # 总共
    total =  disk.f_blocks * disk.f_frsize
    hd['total'] = str(round(total/float(1024*1024*1024), 2)) + " GB"
    # 已使用
    used = total - free
    hd['used'] = str(round(used/float(1024*1024*1024), 2)) + " GB"
    # 使用比例
    hd['used_proportion'] =  (round((total- used) * 100 / total, 2))
    return hd


def db_status():
    """
    获取数据库信息
    """
    db_list = os.listdir(DB_PATH)
    db_ctrl = DB_Ctrl()
    cnt = 0
    result = {}
    for db in db_list:
        if db.endswith(".db"):
            db_info = {}
            db_info["name"] = db
            db_info["size"] = str(int(os.path.getsize(os.path.join(DB_PATH,db))/1024)) + " KB"
            db_info["modify_time"] = get_FileModifyTime(os.path.join(DB_PATH,db))
            db_info["record_cnt"] = db_ctrl.onestep_get_record_cnt(os.path.join(DB_PATH,db))
            db_info["last_record"] = db_ctrl.onestep_get_last_record(os.path.join(DB_PATH,db))
            result[str(cnt)] = db_info
            cnt += 1
    # print(result)
    return result


def get_cpu_temp():
    """
    读取CPU温度
    """
    # output = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
    # pattern = re.compile(r'(?<=temp=)\d+\.?\d*')
    # res = pattern.findall(output)
    # temp = -1
    # if len(res) > 0:
    #     temp = res[0]
    # return  float(temp)
    output = os.popen("cat /sys/class/thermal/thermal_zone0/temp").read()
    temp = round((int(output)/1000),1)
    return temp


def get_mem():
    """
    获取系统内存使用情况
    """
    mem = psutil.virtual_memory()
    EXPAND = 1024 * 1024
    result = {}
    result['total'] = str(round(mem.total / EXPAND, 2)) + " MB"
    result['used'] = str(round(mem.used / EXPAND, 2)) + " MB"
    result['left'] = str(round((mem.total - mem.used) / EXPAND, 2)) + " MB"
    result['used_proportion'] = (round((mem.total - mem.used) * 100/ mem.total, 2))
    return result



def sys_status():
    """
    系统信息
    """
    result = {}
    result['cpu_temp'] = get_cpu_temp()
    result['mem_info'] = get_mem()
    return result


def net_status():
    """
    获取本机mac, ip, mask , gateway
    """
    routingGateway = netifaces.gateways()['default'][netifaces.AF_INET][0]
    routingNicName = netifaces.gateways()['default'][netifaces.AF_INET][1]

    for interface in netifaces.interfaces():
        if interface == routingNicName:
            # print netifaces.ifaddresses(interface)
            routingNicMacAddr = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            try:
                routingIPAddr = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
                # TODO(Guodong Ding) Note: On Windows, netmask maybe give a wrong result in 'netifaces' module.
                routingIPNetmask = netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['netmask']
            except KeyError:
                pass

    ip_list = {'mac': routingNicMacAddr,
                'ip': routingIPAddr,
                'mask': routingIPNetmask,
                'gate': routingGateway}
    return ip_list
