import threading
from timer import Timer
import socket
import numpy as np
import packet


class node:
    def __init__(self, name, port, file, configfile='configfile.txt'):
        self.name = name
        self.port = port
        self.file = file
        self.configFile = configfile
        self.frequency = 0
        self.unreachable = 0
        self.maxValidTime = 0
        self.timerDict = {}  # 节点对应计时器字典
        self.neighbor = []
        self.routeTable = []
        self.isOn = False

        self.ipPort = ('localhost', self.port)
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(self.ipPort)

        # 记录节点信息
        self.LogFile = open("Node_%s_LogFile.txt" % self.name, 'a')

        self.find_neighbor()
        self.config_init()
        self.timer_init()

    # 找邻居, 将邻居ID，距离，端口信息存到neighbor中
    def find_neighbor(self):
        filePath = './case1' + self.file
        with open(filePath, "r") as f:
            data = f.readlines()
        for info in data:
            tmp = info.split(';')
            neighbor = [tmp[0], float(tmp[1]), tmp[2]]
            self.neighbor.append(neighbor)

    # 根据configFile初始化参数
    def config_init(self):
        with open(self.configFile, "r") as f:
            data = f.readlines()
        lst = data[2].split(';')
        self.frequency = int(lst[0])
        self.unreachable = float(lst[1])
        self.maxValidTime = int(lst[2])

    def timer_init(self):  # 每个邻居节点都有一个计时器
        keyList = [tmp[0] for tmp in self.neighbor]
        self.timerDict = {key: Timer(self.maxValidTime/1000) for key in keyList}

    def send_info(self):
        sender = self.receiver
        while True:
            if not self.isOn:
                continue
        if self.isOn:
            info = packet.make(self.name, self.routeTable)  # 制作数据
            for i in self.neighbor:  # 给每个邻居发送路由信息包
                destPort = i[2]  # 获取目标端口号
                destAddr = ('localhost', destPort)
                self.receiver.sendto(info.encode('utf-8'), destAddr)

    def refresh_route_table(self):
        if self.isOn:
            info, addr = self.receiver.recvfrom(4096)  # 接收数据
            switchInfoList = packet.extract(info)
            for perSwitchInfo in switchInfoList:
                destNode = perSwitchInfo[1]
                neighbor = perSwitchInfo[0]
                distance = perSwitchInfo[2]
                # 遍历节点路由表
                for currentTableItem in self.routeTable:





