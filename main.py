import node
import threading


class dvsim():
    def __init__(self):
        self.nodeDict = {}  # 当前存在全部节点
        self.threadDict = {}

    def read_command(self):
        # 读取一条命令
        while True:
            command = input("请输入指令:\n")
            if command != "":
                strlist = command.split(';')
                for i in strlist:
                    if i != '':
                        self.analyse(i)
            # self.analyse(command)

    def analyse(self, command):
        tmp = command.split(' ')
        if tmp[0] == 'init':
            newNode = node.Node(tmp[1], int(tmp[2]), tmp[3])  # 初始化新节点
            self.nodeDict[tmp[1]] = newNode  # 将新建的节点加入字典
        elif tmp[0] == 'start':
            startNodeName = tmp[1]
            self.nodeDict[startNodeName].isOn = True
            self.nodeDict[startNodeName].logFile.write('重新启动该节点\n')

        elif tmp[0] == 'stop':
            stopNodeName = tmp[1]
            self.nodeDict[stopNodeName].isOn = False  # 关闭节点
            self.nodeDict[stopNodeName].logFile.write('关闭该节点\n')


if __name__ == '__main__':
    DVsim = dvsim()
    threading.Thread(target=DVsim.read_command(), args=()).start()
    '''
    init u 50001 u.txt;init v 50002 v.txt;init w 50003 w.txt;init x 50004 x.txt;init y 50005 y.txt;init z 50006 z.txt
    start x
    
    init x 50000 x.txt;init y 50001 y.txt;init z 50002 z.txt
    '''

