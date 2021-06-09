# Distance-Vector
Python 实现一个基于 DV 算法的路由选择协议，根据网络状态定期更新路由表。



## 需要实现的功能

* 根据节点初始化文件和配置文件进行路由器初始化
* 路由器节点维护路由表



## Node类

定义每个路由器节点

### 1. 变量

* 初始化时的变量：
  * `name`: 路由器ID
  * `port`: 路由器对应UDP端口
  * `initFile`: 路由器使用的初始化文件
  * `configFile`: 路由器使用的配置文件
* 类内定义变量
  * 读取`configFile`后获取的变量
    * `self.frequency`
    * `self.unreachable`
    * `self.maxValidTime`
  * `self.timerList`: 节点计时器列表
  * `self.neighbor`: 将初始化列表中的邻居信息备份
  * `self.routeTable`
  * `self.isOn = 1`: 表示存储器正处于运行状态
  * `self.sendSequenceNumber`: 发送包的序列号
  * `self.recvSequenceNumber`: 接收包的序列号 
* 交换的路由信息
  * `SrcNode`: 发送节点的ID(该值会成为路由表中Neighbor值)
  * `DestNode`: 目的节点的ID
  * `Distance`: 发送节点到达目的节点的距离

* 节点维护的路由表
  * `DestNode`: 目的地节点ID
  * `Distance`: 自身到达目的节点所需的距离
  * `Neighbor`: 下一跳路由器节点ID, 若直达, 该变量值为目的地节点ID

### 2. 方法

* `def send_info(self.isOn, self.neighbor, self.routeTable)`
  * 功能: 如果当前节点处于活动状态, 向该节点的所有邻居发送路由信息
  * 参数: 
    * `neighbor`: 节点邻居列表
    * `routeTable`: 节点路由表
  * 无返回值

* `def refreshRouteTable(switchInfoList)`
  * 功能: 根据收到的路由信息更新本节点路由表
  * 实现：
    * 将发来的**路由更新信息**转换成**路由表**格式：将路由表中的下一跳（路由表的neighbor）设置为路由信息中srcNode
    * 根据转换得到的路由表中的每个项目：
      * 若原表中没有destNode，填入路由表
      * 如果原表中有destNode，查看下一跳路由器ID：如果原表下一跳和转换得到表下一跳相同，直接替换项目；如果不相同，如果新距离比较近就更新，否则不做处理
      * 如果xx秒没有收到相邻路由器的更新路由表，则把其设为不可达路由器，对应neighbor中的值也会修改
  * 返回值: RouteTable(更新后的路由表)

## packet类

定义路由表信息打包和解包方法

* `packet.make(currentNode, self.routeTable)` 

  * 功能: 使用路由表制作交换路由信息

  * 参数: 节点当前路由表(List)

    e.g: 当前节点ID为c, 路由表如下

    `[[a, 10.0, b], [d, 10.0, b]]`

  * 返回值: 交换的路由信息(String)

    `'c;a;10&c;d;10'`

* `packet.extract(self.switchInfo)` 

  * 功能: 提取交换路由信息中内容
  * 参数: switchInfo(交换路由信息(String))
  * 返回值: switchInfoList(路由信息的List形式(List))

