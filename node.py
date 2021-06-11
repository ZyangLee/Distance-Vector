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
        self.neighbor = {}  # 目前只存端口号
        self.routeTable = {}
        self.isOn = True
        self.routeTableLock = threading.Lock()
        # 网络端口初始化
        self.ipPort = ('localhost', self.port)
        self.sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiver.bind(self.ipPort)

        # 记录节点信息
        self.logFile = open("Node_%s_LogFile.txt" % self.name, 'w+')
        self.sendNum = 0
        self.receiveNum = 0

        self.find_neighbor()
        self.config_init()
        self.timer_init()
        strTmp = get_time_string()
        self.logFile.write(strTmp + 'Initialize Success\n')
        print(f'node {self.name}, Initialize Success')

        # 运行多线程，收包和发包
        threading.Thread(target=self.send_info, args=()).start()
        threading.Thread(target=self.receive_info, args=()).start()
        threading.Thread(target=self.check, args=()).start()
        threading.Thread(target=self.display, args=()).start()

    # 找邻居, 将邻居ID，距离，端口port信息存到neighbor中, 同时初始化
    def find_neighbor(self):
        self.routeTableLock.acquire()
        filePath = './case1/' + self.file
        with open(filePath, "r") as f:
            data = f.readlines()
        for info in data:
            tmp = info.split(';')
            self.neighbor[tmp[0]] = int(tmp[2])  # neighbor字典中value为指定节点端口号
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
        while True:
            if not self.isOn:
                continue
            self.routeTableLock.acquire()
            self.sendNum += 1
            head = f'## Send.Source Node={self.name}; Sequence Number={self.sendNum}\n'
            logMessage = self.makeLog(self.routeTable)
            self.logFile.write(head + logMessage)
            # print(head + logMessage, end='')
            info = packet.make(self.name, self.routeTable)  # 制作数据
            for name in self.neighbor:  # 给每个邻居发送路由信息包
                destPort = self.neighbor[name]  # 获取目标端口号
                destAddr = ('localhost', destPort)
                self.sender.sendto(info.encode('utf-8'), destAddr)
            self.routeTableLock.release()
            time.sleep(self.frequency/1000)  # 每三秒向所有邻居发送该时刻的路由表

    def refresh_route_table(self, info, routeTable):
        # 记录接收的包裹
        switchInfoList = packet.extract(info)
        receiveRouteTable = {}
        for perSwitchInfo in switchInfoList:
            destNode = perSwitchInfo[2]  # 目的节点
            if destNode == self.name:  # 如果目的节点是自己，直接跳过
                continue
            neighbor = perSwitchInfo[0]  # 下一跳
            distance = float(perSwitchInfo[1]) + routeTable[neighbor][0]  # 距离
            receiveRouteTable = {destNode: [neighbor, distance]}
            self.timerDict[neighbor].refresh()  # 收到邻居路由器消息，重置该邻居计时器
            # 原路由表中没有destNode，则添加
            if destNode not in routeTable:
                routeTable[destNode] = [distance, neighbor]
            elif routeTable[destNode][1] == neighbor:  # 原路由表的下一跳路由器和转换得到表的下一跳相同，直接替换
                routeTable[destNode] = [distance, neighbor]
                # 如果信息中距离小于原表的距离才进行替换
            elif distance < self.routeTable[destNode][0]:
                routeTable[destNode] = [distance, neighbor]
        return routeTable, receiveRouteTable

    def receive_info(self):
        for node in self.timerDict:  # 启动所有定时器
            self.timerDict[node].start()
        while True:
            if not self.isOn:
                continue
            info = self.receiver.recv(2048).decode('utf-8')
            self.routeTableLock.acquire()
            self.routeTable, receivedRouteTable = self.refresh_route_table(info, self.routeTable)
            # 记录刚才接收到的包裹
            self.receiveNum += 1
            logMessageHead = f'###Received. Dst Node={self.name}; Sequence number={self.receiveNum}\n'
            self.logFile.write(get_time_string() + logMessageHead + self.makeLog(receivedRouteTable))
            # print(logMessageHead + self.makeLog(receivedRouteTable))
            self.routeTableLock.release()


    def set_invalid_node(self):
        for node in self.timerDict:
            if self.timerDict[node].timeout():
                self.routeTable[node] = [self.unreachable, node]

    def makeLog(self, routeTable):
        # 将一个字典型的信息转换成日志文件中的记录
        tmp = ''
        for name in routeTable:
            tmp += f'DestNode={name}; Distance={self.routeTable[name][0]}; Neighbor={self.routeTable[name][1]}\n'
        return tmp

    def check(self):
        while True:
            if not self.isOn:
                continue
            time.sleep(9)
            # 每隔9秒检查是否有计时器超时
            self.routeTableLock.acquire()
            for node in self.timerDict:  # 遍历所有邻居节点，查看他们的计时器是否超时
                if self.timerDict[node].timeout():
                    # print(f'{self.name}的邻居节点{node}已经被关闭')
                    self.logFile.write(f'{self.name}的邻居节点{node}已经被关闭\n')
                    for tmp in self.routeTable:
                        if self.routeTable[tmp][1] == node or node == tmp:
                            self.routeTable[tmp][0] = self.unreachable
            self.routeTableLock.release()

    def display(self):
        while True:
            # if self.name != 'z':  # 单独测试一个节点
            #     break
            if not self.isOn:
                continue
            self.routeTableLock.acquire()
            # print(self.name, "的结点情况如下:")
            for node in self.routeTable:
                tmp = f'终点：{node}, 距离：{self.routeTable[node][0]},'\
                      f'下一跳：{self.routeTable[node][1]}\n'
                # print(tmp, end='')
                self.logFile.write(tmp)
            self.routeTableLock.release()
            time.sleep(10)


def get_time_string():
    datestring = "% d. % d. % d" % (time.localtime(time.time()).tm_year,
                                    time.localtime(time.time()).tm_mon,
                                    time.localtime(time.time()).tm_mday)
    timestring = "%4d/%2d/%2d %2d:%2d:%2d " % (
        time.localtime(time.time()).tm_year, time.localtime(time.time()).tm_mon,
        time.localtime(time.time()).tm_mday,
        time.localtime(time.time()).tm_hour, time.localtime(time.time()).tm_min,
        time.localtime(time.time()).tm_sec
    )
    return datestring + " " + timestring + "\n"



