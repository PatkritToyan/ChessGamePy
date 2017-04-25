# -*- coding:utf-8 -*-
import logging


class TableShowService(object):

    SERVICE_ID = 100

    def __init__(self):
        # 每张桌子现有人数列表
        self.tableList = [0 for x in range(100)]
        # 显示每张桌子的用户列表
        self.userList = []
        # 显示每个用户当前的状态
        self.state = {}
        # 每个用户的得分列表
        self.scoreList = {}
        for i in range(25):
            self.userList.append([])
        commands = {
            1001: self.getTableList,
            1002: self.userIn,
            1003: self.userOut,
            1004: self.getOpponent,
            1005: self.setState,
            1006: self.updateChess,
            1007: self.getWinner,
            1008: self.giveUp,
            1009: self.getScoreList
        }
        self.registers(commands)

    def handle(self, msg):
        cid = msg['cid']
        if not cid in self.__command_map:
            raise Exception('bad command %s' % cid)
        f = self.__command_map[cid]
        return f(msg)

    def register(self, cid, function):
        self.__command_map[cid] = function

    def registers(self, CommandDict):
        self.__command_map = {}
        for cid in CommandDict:
            self.register(cid, CommandDict[cid])
        return 0

    # 获得每张桌子的人数
    def getTableList(self, msg):
        data = {'sid': 100, 'cid': 1001, 'tableList': self.tableList, 'sendType': 1}
        return data

    # 玩家进入房间 初始化得分dict
    def userIn(self, msg):
        numOfTable = msg['roomid'] * 5 + msg['tableid']
        if self.tableList[numOfTable] < 2:
            self.tableList[numOfTable] += 1
        self.userList[numOfTable].append(msg['user'])
        self.state[msg['user']] = 'notReady'
        if msg['user'] in self.scoreList.keys() and self.scoreList[msg['user']] != 0:
            pass
        else:
            self.scoreList[msg['user']] = 0
        data = {'sid': 100, 'cid': 1001, 'tableList': self.tableList, 'sendType': 1}
        return data

    # 玩家离开房间
    def userOut(self, msg):
        numOfTable = msg['roomid'] * 5 + msg['tableid']
        if self.tableList[numOfTable] > 0:
            self.tableList[numOfTable] -= 1
        self.userList[numOfTable].remove(msg['user'])
        if msg['opponent'] != None:
            msg['userlist'] = [msg['opponent']]
        else:
            msg['userlist'] = []
        msg['sendType'] = 3
        self.state[msg['user']] = 'leave'
        return msg

    # 获取对手信息
    def getOpponent(self, msg):
        numOfTable = msg['roomid'] * 5 + msg['tableid']
        opponent = ''
        for i in self.userList[numOfTable]:
            if i != msg['user']:
                opponent = i
        data = {'sid': 100, 'cid': 1004, 'opponent': opponent, 'sendType': 1}
        return data

    # 设置状态
    def setState(self, msg):
        state = msg['message']
        name = msg['user']
        self.state[name] = state
        if self.state[msg['opponent']] == 'begin':
            return {'sid': 100, 'cid': 1005, 'message': 'begin', 'userlist': [msg['user'], msg['opponent']],
                    'sendType': 3, 'white': msg['opponent']}
        else:
            return {'sid': 100, 'cid': 1005, 'message': 'nobegin', 'userlist': [msg['user'], msg['opponent']],
                    'sendType': 3}

    # 告知对手开始游戏
    def updateChess(self, msg):
        msg['sendType'] = 3
        return msg

    # 获知胜利结果
    def getWinner(self, msg):
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
        logging.debug("SERVER getWinner() scoreList:%s" % self.scoreList)
        winner = msg['winner']
        self.scoreList[winner] += 6
        loser = msg['loser']
        self.scoreList[loser] += 1
        msg['userlist'] = [msg['loser']]
        msg['sendType'] = 3
        return msg

    # 某方认输
    def giveUp(self, msg):
        winner = msg['winner']
        self.scoreList[winner] += 6
        loser = msg['loser']
        self.scoreList[loser] += 1
        msg['userlist'] = [msg['winner']]
        msg['sendType'] = 3
        return msg

    # 获得分数列表
    def getScoreList(self, msg):
        data = {'sid': 100, 'cid': 1009, 'scorelist': self.scoreList, 'sendType': 2}
        return data