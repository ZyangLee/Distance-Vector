import node
import threading


class dvsim():
    def __init__(self):
        self.nodeDict = {}  # 当前存在全部节点

    def read_command(self):
        # 读取一条命令
        while True:
            command = input("请输入指令:")
            self.analyse(command)

    def analyse(self, command):
        tmp = command.split(' ')
        if tmp[0] == 'init':
            newNode = node.Node(tmp[1], tmp[2], tmp[3])  # 初始化新节点
            self.nodeDict[tmp[1]] = newNode  # 将新建的节点加入字典
        elif tmp[0] == 'start':
            startNodeName = tmp[1]
            pass  # 新建该节点进程的进程
        elif tmp[0] == 'stop':
            stopNodeName = tmp[1]
            pass  # 结束对应节点的进程


