def make(currentNode, routeTable):
    info = ''
    for key in routeTable:
        info_single = f'{currentNode};{routeTable[key][0]};{routeTable[key][1]}&'
        info += info_single
    return info[:-1]


def extract(switchInfo):
    data = switchInfo.split('&')
    switchInfoList = []
    for info in data:
        tmp = info.split(';')
        # srcNode = tmp[0]
        # DestNode = tmp[1]
        # Distance = tmp[2]
        tmpList = [tmp[0], tmp[1], tmp[2]]
        switchInfoList.append(tmpList)
    return switchInfoList


