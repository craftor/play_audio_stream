# udp_gb_server.py
'''服务端（UDP协议局域网广播）'''

import socket
import uuid

class udp_sender(object):

    def __init__(self, port):
        """
        初始化
        """
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.ss.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.PORT = port
        self.network = '<broadcast>'

    def get_ip(self):
        """
        获取本机IP
        """

    def get_mac_address(self):
        """
        获取mac地址
        """
        mac=uuid.UUID(int = uuid.getnode()).hex[-12:] 
        return ":".join([mac[e:e+2] for e in range(0,11,2)])

    def gen_ip_change_cmd(self, dest_mac, dest_ip, dest_mask, dest_gateway):
        """
        生成改ip的命令包
        """
        cmd_list = []
        cmd_list.append('change_ip')
        cmd_list.append(dest_mac)
        cmd_list.append(dest_ip)
        cmd_list.append(dest_mask)
        cmd_list.append(dest_gateway)
        return self.list2str(cmd_list)

    def list2str(self, cmd_list):
        """
        List 转 Str
        """
        str = ""
        for each in cmd_list:
            str += each + "|"
        return str

    def send_cmd(self, cmd):
        """
        发送命令
        """
        self.ss.sendto(cmd.encode('utf-8'), (self.network, self.PORT))

    def run(self):
        """
        运行
        """
        cmd = self.gen_ip_change_cmd('b8:27:eb:80:a9:d1', '192.168.1.80', '255.255.255.0', '192.168.1.1')
        self.send_cmd(cmd)

if __name__ == "__main__":
    sender = udp_sender(1060)
    sender.run()