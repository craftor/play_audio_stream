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

    def run(self):
        """
        运行
        """
        mac = self.get_mac_address()
        # print(mac)
        self.ss.sendto(mac.encode('utf-8'), (self.network, self.PORT))


if __name__ == "__main__":
    sender = udp_sender(1060)
    sender.run()