import threading
from timer import Timer
import socket
import packet
import time


class Node:
    def __init__(self, name, port, file, configfile='configfile.txt'):
        self.name = name
        self.port = port
        self.file = file
        self.configFile = configfile
        self.frequency = 0
        self.unreachable = 0
        self.maxValidTime = 0
        self.timerDict = {}  # 节点对应计时器字典
        self.neighbor = {}
        self.routeTable = {}
        self.isOn = False
        self.routeTableLock = threading.Lock()
        # 网络端口初始化
        self.ipPort = ('localhost', self.port)
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(self.ipPort)

        # 记录节点信息
        self.LogFile = open("Node_%s_LogFile.txt" % self.name, 'a')

        self.find_neighbor()
        self.config_init()
        self.timer_init()

    # 找邻居, 将邻居ID，距离，端口port信息存到neighbor中, 同时初始化
    def find_neighbor(self):
        self.routeTableLock.acquire()
        filePath = './case1' + self.file
        with open(filePath, "r") as f:
            data = f.readlines()
        for info in data:
            tmp = info.split(';')
            self.neighbor[tmp[0]] = tmp[2]  # neighbor字典中value为指定节点端口号
            self.routeTable[tmp[0]] = [float(tmp[1]), tmp[0]]
        self.routeTableLock.release()

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
            info = packet.make(self.name, self.routeTable)  # 制作数据
            for i in self.neighbor:  # 给每个邻居发送路由信息包
                destPort = i[2]  # 获取目标端口号
                destAddr = ('localhost', destPort)
                sender.sendto(info.encode('utf-8'), destAddr)

    def refresh_route_table(self, info, routeTable):
        switchInfoList = packet.extract(info)
        for perSwitchInfo in switchInfoList:
            destNode = perSwitchInfo[1]  # 目的节点
            neighbor = perSwitchInfo[0]  # 下一跳
            distance = perSwitchInfo[2] + self.routeTable[neighbor][0]  # 距离
            self.timerDict[neighbor].stop()  # 收到邻居路由器消息，停止该邻居计时器
            # 原路由表中没有destNode，则添加
            if destNode not in routeTable:
                routeTable[destNode] = [distance, neighbor]
            else:  # 原路由表中有destNode需要进行判断
                # 原路由表的下一跳路由器和转换得到表的下一跳相同，直接替换
                if routeTable[destNode][1] == neighbor:
                    routeTable[destNode] = [distance, neighbor]
                # 如果信息中距离小于原表的距离才进行替换
                elif distance < self.routeTable[destNode][0]:
                    routeTable[destNode] = [distance, neighbor]
        return routeTable

    def receive_info(self):
        for node in self.timerDict:
            self.timerDict[node].start()

        while True:
            info = self.receiver.recv(2048).decode('utf-8')
            self.routeTableLock.acquire()
            self.routeTable = self.refresh_route_table(info, self.routeTable)
            self.set_invalid_node()
            self.routeTableLock.release()

    def set_invalid_node(self):
        for node in self.timerDict:
            if self.timerDict[node].timeout():
                self.routeTable[node] = [self.unreachable, node]




