# -*- coding: utf-8 -*-


import locale, sys, json, time, images
from server import netstream
from server.ChessBoard import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from UI_ChessGame import Ui_MainWindow
import logging

# from server import ChessBoard


default_code = 'utf-8'
c = QString(locale.getdefaultlocale()[0]).toLower()
if c.contains('zh_cn'):
    default_code = 'gbk'
elif c.contains('zh_tw'):
    default_code = 'big5'
else:
    default_code = 'gb2312'
try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s
try:
    _toUtf8 = QString.toUtf8
except AttributeError:
    def _toUtf8(s):
        return s


class ChessGame(QMainWindow, Ui_MainWindow):
    def __init__(self, ip, port, username, ns):
        QMainWindow.__init__(self, None)
        self.ip = ip
        self.port = port
        self.username = username
        self.ns = ns

    # 初始化配置信息
    def __init__config(self):
        # 显示每张桌子现有人数
        self.tableList = [0 for i in range(100)]
        # 得分情况
        self.scoreList = {}
        self.timer = QTimer()
        self.loopCnt = 40
        self.tickCnt = 100
        # 默认第一次进入大厅
        self.FirstTime = True

    # 初始化UI
    def __init__ui(self):
        self.setupUi(self)
        self.setWindowTitle(_fromUtf8(self.username))
        self.setUiStyleSheet()
        self.userInfo = ChessBoard(self.username, self.chessboard, self.infotext)
        self.setButtonStatus(False, False, False, False, False, False)
        # 设置聊天框只读
        self.singleChatEdit.setReadOnly(True)
        self.singleChatRoom.setReadOnly(True)
        self.groupChatRoom.setReadOnly(True)
        self.connect(self.readyBt, SIGNAL("clicked()"), self.readyChess)
        self.connect(self.giveUpBt, SIGNAL("clicked()"), self.giveUpChess)
        self.connect(self.peaceBt, SIGNAL("clicked()"), self.peaceChess)
        self.connect(self.againBt, SIGNAL("clicked()"), self.againChess)
        self.connect(self.leaveOutBt, SIGNAL("clicked()"), self.leaveOutChess)
        self.connect(self.closeBt, SIGNAL("clicked()"), self.outofServer)
        self.connect(self.miniBt, SIGNAL("clicked()"), self.showMinimized)
        self.connect(self.sendGroupMsg, SIGNAL("clicked()"), self.sendGroupMsgEvent)
        self.connect(self.sendSingleMsg, SIGNAL("clicked()"), self.sendSingleMsgEvent)
        self.hallList.itemDoubleClicked.connect(self.intoTable)
        # 触发定时器
        self.connect(self.timer, SIGNAL("timeout()"), self.check)

    #退出客户端
    def outofServer(self):
        data = {'sid': 110, 'user': self.userInfo.name}
        self.ns.send(json.dumps(data))
        if self.userInfo.IsInRoom:
            self.userInfo.IsInRoom = False
            msg = {'sid': 100, 'cid': 1003, 'roomid': self.userInfo.roomId - 1,
                   'tableid': self.userInfo.tableId - 1, 'user': self.userInfo.name,
                   'opponent': self.userInfo.opponent}
            self.ns.send(json.dumps(msg))
        self.close()
    # 连接服务器
    def connectToServer(self):
        self.__init__config()
        self.__init__ui()
        self.timer.start(50)

    def setUiStyleSheet(self):
        icon = QIcon()
        icon.addPixmap(QPixmap(_fromUtf8(":/images/chesslogo.png")), QIcon.Normal, QIcon.Off)
        self.setWindowIcon(icon)
        self.appName.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 18px; font-weight: bold; color: #FF6A6A"))
        self.textEdit_3.setStyleSheet(_fromUtf8("font-family: 宋体; font-size: 12px; color: #8B2500"))
        self.rule.setStyleSheet(_fromUtf8("font-family: Papyrus; font-size: 14px; font-weight: bold; color: #FF6A6A"))
        self.singleRoomChatTitle.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 14px; font-weight: bold; color: #FF6A6A"))
        self.groupChatTitle.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 14px; font-weight: bold; color: #FF6A6A"))
        self.userRankList.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 14px; font-weight: bold; color: #FF6A6A"))
        self.hallList.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 12px; font-weight: bold; color: #FF6A6A"))
        self.userone.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 12px; font-weight: bold; color: #FF6A6A"))
        self.usertwo.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 12px; font-weight: bold; color: #FF6A6A"))
        self.scoreStatus1.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 14px; font-weight: bold; color:#8B1A1A"))
        self.scoreStatus2.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 14px; font-weight: bold; color:#8B1A1A"))
        self.scoreListWigdet.setStyleSheet(
            _fromUtf8("font-family: Papyrus; font-size: 14px; font-weight: bold; color:#9ACD32")
        )

    def setButtonStatus(self, readyStatus, giveupStatus, peaceStatus, againStatus, leaveoutStatus, singleChatStatus):
        self.readyBt.setEnabled(readyStatus)
        self.giveUpBt.setEnabled(giveupStatus)
        self.peaceBt.setEnabled(peaceStatus)
        self.againBt.setEnabled(againStatus)
        self.leaveOutBt.setEnabled(leaveoutStatus)
        self.sendSingleMsg.setEnabled(singleChatStatus)

    # 开始准备
    def readyChess(self):
        self.setButtonStatus(False, True, False, False, False, True)
        self.userInfo.IsReady = True
        msg = {'sid': 100, 'cid': 1005, 'message': 'begin', 'user': str(self.userInfo.name),
               'opponent': self.userInfo.opponent}
        self.ns.send(json.dumps(msg))

    # 认输
    def giveUpChess(self):
        self.setButtonStatus(False, False, False, True, True, True)
        self.userInfo.IsNext = False
        msg = {'sid': 100, 'cid': 1008, 'winner': self.userInfo.opponent, 'loser': self.userInfo.name,
               'chessType': self.userInfo.chessType}
        self.ns.send(json.dumps(msg))
        self.ns.process()
        self.infotext.setText(_fromUtf8('你认输了'))

    # 和棋
    def peaceChess(self):
        msg = {'sid': 104, 'cid': 1003, 'message': 'peace', 'userlist': [self.userInfo.opponent],
               'user': self.userInfo.name}
        self.ns.send(json.dumps(msg))

    # 再玩一局
    def againChess(self):
        msg = {'sid': 104, 'cid': 1001, 'message': 'again', 'userlist': [self.userInfo.opponent],
               'user': self.userInfo.name}
        self.ns.send(json.dumps(msg))

    # 离开房间
    def leaveOutChess(self):
        self.userInfo.clearChessBoard()
        self.userInfo.IsInRoom = False
        msg = {'sid': 100, 'cid': 1003, 'roomid': self.userInfo.roomId - 1,
               'tableid': self.userInfo.tableId - 1, 'user': self.userInfo.name,
               'opponent': self.userInfo.opponent}
        self.ns.send(json.dumps(msg))
        self.ns.process()
        self.userInfo.tableId = -1
        self.userInfo.roomId = -1
        self.setButtonStatus(False, False, False, False, False, False)
        self.userone.setText(_fromUtf8("玩家一"))
        self.scoreStatus1.setText("0" + _fromUtf8("分"))
        self.usertwo.setText(_fromUtf8("玩家二"))
        self.scoreStatus2.setText("0" + _fromUtf8("分"))
        self.roomName.setText(_fromUtf8("暂未进入房间"))
        self.infotext.setText(_fromUtf8("你已经离开房间"))
        self.userInfo.clearChessBoard()

    # 进入房间
    def intoTable(self, item):
        # 已经在房间了，点击无效
        if self.userInfo.IsInRoom:
            return
        parent_table = item.parent()
        # 桌子序号
        numOfTable = -1
        if parent_table:
            numOfTable = parent_table.indexOfChild(item)
        parent_room = parent_table.parent()
        # 房间序号
        numOfRoom = -1
        if parent_room:
            numOfRoom = parent_room.indexOfChild(parent_table)
        if numOfRoom != -1:
            # 桌子序号
            index = numOfRoom * 10 + numOfTable
            # 获取桌子在座的人数
            numOfPlay = self.tableList[index]
            if numOfPlay == 2:
                QMessageBox.information(self, _fromUtf8('提示'), _fromUtf8("桌子人数已满，请选择其它桌子！"))
            elif numOfPlay == 1:
                QMessageBox.information(self, _fromUtf8('提示'), _fromUtf8("你已经进入房间，马上开始游戏吧！"))
                msg = {'sid': 100, 'cid': 1002, 'roomid': numOfRoom, 'tableid': numOfTable, 'user': self.username}
                self.ns.send(json.dumps(msg))
                self.userInfo.IsInRoom = True
                self.setButtonStatus(True, False, False, False, True, True)
                self.userInfo.roomId = numOfRoom + 1
                self.userInfo.tableId = numOfTable + 1
                self.roomName.setText(
                    _fromUtf8('房间') + str(self.userInfo.roomId) + _fromUtf8('\n桌子') + str(self.userInfo.tableId))
                self.infotext.setText(_fromUtf8('欢迎你坐下！'))
                self.userone.setText(_fromUtf8(self.userInfo.name))
                # 获取对手的资料
                msg1 = {'sid': 100, 'cid': 1004, 'roomid': numOfRoom, 'tableid': numOfTable, 'user': self.username}
                self.ns.send(json.dumps(msg1))
                self.ns.process()
                msg2 = {'sid': 100, 'cid': 1009}
                self.ns.send(json.dumps(msg2))
                self.ns.process()
            else:
                QMessageBox.information(self, _fromUtf8("提示"), _fromUtf8("您已进入房间，等待您的对手进入房间！"))
                print "inRoom" + self.username
                data = {'sid': 100, 'cid': 1002, 'roomid': numOfRoom, 'tableid': numOfTable, 'user': self.username}
                self.ns.send(json.dumps(data))
                self.ns.process()
                self.userInfo.IsInRoom = True
                self.userInfo.opponent = None
                self.setButtonStatus(False, False, False, False, True, True)
                self.singleChatEdit.setReadOnly(False)
                self.userInfo.roomId = numOfRoom + 1
                self.userInfo.tableId = numOfTable + 1
                self.roomName.setText(
                    _fromUtf8('房间') + str(self.userInfo.roomId) + _fromUtf8('\n桌子') + str(self.userInfo.tableId))
                self.infotext.setText(_fromUtf8('欢迎您'))
                self.userone.setText(_fromUtf8(self.userInfo.name))
                msg2 = {'sid': 100, 'cid': 1009}
                self.ns.send(json.dumps(msg2))
                self.ns.process()

    # 客户端轮询
    def check(self):
        self.client_config()
        self.ns.process()
        if self.ns.status() == netstream.NET_STATE_ESTABLISHED:
            data = self.ns.recv()
            if len(data) > 0:
                data = json.loads(data)
                # 查询能否进入房间
                if data['sid'] == 100:
                    if data['cid'] == 1001:
                        self.tableList = data['tableList']
                    elif data['cid'] == 1003:
                        if data['roomid'] == self.userInfo.roomId - 1 and data['tableid'] == self.userInfo.tableId - 1:
                            self.infotext.setText(_fromUtf8('您的对手离开了房间'))
                            self.setButtonStatus(False, False, False, False, True, False)
                            self.userInfo.opponent = None
                            self.usertwo.setText(_fromUtf8('玩家二'))
                            self.scoreStatus2.setText(_fromUtf8('0 分'))
                    elif data['cid'] == 1004:  # 对手进来了 获取对手信息
                        if data['opponent'] != '':
                            self.userInfo.opponent = data['opponent']
                            self.usertwo.setText(_fromUtf8(self.userInfo.opponent))
                            self.singleChatEdit.setReadOnly(False)
                            self.setButtonStatus(True, False, False, False, True, True)
                            if not self.userInfo.opponent in self.scoreList.keys():
                                self.scoreStatus2.setText("0 " + _fromUtf8("分"))
                            else:
                                self.scoreStatus2.setText(str(self.scoreList[self.userInfo.opponent]) + _fromUtf8("分"))
                            self.scoreStatus2.update()
                    elif data['cid'] == 1005:
                        if data['message'] == u'begin':
                            # 开始比赛
                            self.GoingChess(data)
                        else:
                            self.infotext.setText(_fromUtf8('还有一方未准备!'))
                    elif data['cid'] == 1006:
                        n = data['n']
                        m = data['m']
                        self.userInfo.chessCnt = data['chesscnt']
                        self.userInfo.updateChessBoard(n, m)
                    elif data['cid'] == 1007:
                        self.infotext.setText(_fromUtf8("很遗憾，你输了"))
                        self.setButtonStatus(False, False, False, True, True, True)
                        self.userInfo.IsNext = False
                        msg = {'sid': 100, 'cid': 1009}
                        self.ns.send(json.dumps(msg))
                        self.ns.process()
                    elif data['cid'] == 1008:
                        self.infotext.setText(_fromUtf8("对方认输，你赢了"))
                        self.setButtonStatus(False, False, False, True, True, True)
                        self.userInfo.IsNext = False
                        msg = {'sid': 100, 'cid': 1009}
                        self.ns.send(json.dumps(msg))
                        self.ns.process()
                    elif data['cid'] == 1009:
                        self.scoreList = data['scorelist']
                        # 更新排行榜
                        self.rank()
                        # 更新得分显示
                        self.updateScore()
                    elif data['cid'] == 1010:
                        self.infotext.setText(_fromUtf8("和棋！"))
                        self.setButtonStatus(False, False, False, True, True, True)
                        self.userInfo.IsNext = False
                        self.userInfo.chessCnt = 0
                        msg = {'sid': 100, 'cid': 1009}
                        self.ns.send(json.dumps(msg))
                        self.ns.process()
                elif data['sid'] == 101:
                    self.infotext.setText(_fromUtf8("欢迎你进入大厅"))
                    self.groupChatEdit.setReadOnly(False)
                    self.sendGroupMsg.setEnabled(True)
                elif data['sid'] == 104:
                    if data['cid'] == 1001:
                        replay = QMessageBox.question(self, _fromUtf8("再玩一局"), _fromUtf8("你的对手请求再来一局，是否同意？"),
                                                      QMessageBox.Yes, QMessageBox.No)
                        if replay == QMessageBox.Yes:
                            data = {'sid': 104, 'cid': 1002, 'replay': 'yes', 'userlist': [self.userInfo.opponent],
                                    'white': self.userInfo.name.decode('utf-8')}
                            self.ns.send(json.dumps(data))
                            self.ns.process()
                            # 清除棋盘
                            self.userInfo.clearChessBoard()
                            # 正式开始比赛
                            self.GoingChess(data)
                        else:
                            data = {'sid': 104, 'cid': 1002, 'replay': 'no', 'userlist': [self.userInfo.opponent]}
                            self.ns.send(json.dumps(data))
                            self.ns.process()
                    elif data['cid'] == 1002:
                        if data['replay'] == 'yes':
                            QMessageBox.information(self, _fromUtf8("提示"), _fromUtf8("对手同意再来一局"))
                            # 清除棋盘
                            self.userInfo.clearChessBoard()
                            # 正式开始比赛
                            self.GoingChess(data)
                        else:
                            QMessageBox.information(self, _fromUtf8("提示"), _fromUtf8("对手拒绝了你的请求"))
                    elif data['cid'] == 1003:
                        replay = QMessageBox.question(self, _fromUtf8("和棋"), _fromUtf8("你的对手请求和棋，是否同意？"),
                                                      QMessageBox.Yes, QMessageBox.No)
                        if replay == QMessageBox.Yes:
                            self.userInfo.IsNext = False
                            data = {'sid': 104, 'cid': 1004, 'replay': 'yes', 'userlist': [self.userInfo.opponent]}
                            self.ns.send(json.dumps(data))
                            self.ns.process()
                        else:
                            data = {'sid': 104, 'cid': 1004, 'replay': 'no', 'userlist': [self.userInfo.opponent]}
                            self.ns.send(json.dumps(data))
                            self.ns.process()
                    elif data['cid'] == 1004:
                        if data['replay'] == 'yes':
                            self.userInfo.IsNext = False
                            QMessageBox.information(self, _fromUtf8("提示"), _fromUtf8("对手同意和棋"))
                            data = {'sid': 100, 'cid': 1010, 'userlist': [self.userInfo.opponent, self.userInfo.name]}
                            self.ns.send(json.dumps(data))
                            self.ns.process()
                        else:
                            QMessageBox.information(self, _fromUtf8("提示"), _fromUtf8("对手拒绝了你的请求"))
                elif data['sid'] == 105:
                    pass
                elif data['sid'] == 106:
                    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    QDateTime.fromString(now_time, 'yyyy-MM-dd hh:mm:ss')
                    if data['cid'] == 1003:
                        if data['user'] != self.userInfo.name.decode('utf-8'):
                            self.singleChatRoom.append(now_time + '\n' + self.userInfo.opponent + ":" + data['message'])
                        else:
                            self.singleChatRoom.append(now_time + '\n' + self.userInfo.name.decode('utf-8') + ":" + data['message'])
                        self.singleChatRoom.update()
                        self.singleChatEdit.clear()
                        self.singleChatEdit.update()
                    elif data['cid'] == 1001:
                        if data['user'] != self.userInfo.name.decode('utf-8'):
                            self.groupChatRoom.append(now_time + '\n' + data['user'] + ":" + data['message'])
                        else:
                            self.groupChatRoom.append(now_time + '\n' + data['user'] + ":" + data['message'])
                        self.groupChatRoom.update()
                        self.groupChatEdit.clear()
                        self.groupChatEdit.update()
                elif data == 'quit':
                    self.ns.close()
                    shutdown = True
                else:
                    pass
            else:
                pass
        elif self.ns.status() == netstream.NET_STATE_STOP:
            pass

    # 客户端配置
    def client_config(self):
        # 更新房间桌子列表
        self.updateRoom()
        # 检索对手
        if self.userInfo.opponent == None and self.loopCnt == 0:
            self.loopCnt = 40
            if self.userInfo.tableId != -1:
                data1 = {'sid': 100, 'cid': 1004, 'roomid': self.userInfo.roomId - 1,
                         'tableid': self.userInfo.tableId - 1,
                         'user': self.userInfo.name}
                self.ns.send(json.dumps(data1))
                self.ns.process()
        else:
            if self.loopCnt == 0:
                self.loopCnt = 40
            self.loopCnt -= 1

        # 每隔5s发送一次心跳包
        if self.tickCnt == 0:
            self.tickCnt = 100
            data2 = {'sid': 105, 'cid': 1001}
            self.ns.send(json.dumps(data2))
            self.ns.process()
        else:
            self.tickCnt -= 1

    # 更新桌子列表
    def updateRoom(self):
        # invisibelRootItem()得到的是所有节点的最终根节点
        self.hallList.setHeaderLabel(_fromUtf8("大厅"))
        itemAncestor = self.hallList.invisibleRootItem()
        itemHall = itemAncestor.child(0)
        itemHall.setText(0, '房间列表'.decode('utf-8'))
        roomCnt = itemHall.childCount()
        for i in range(0, roomCnt):
            itemRoom = itemHall.child(i)
            index = 0
            # 一个房间10个桌子
            for j in range(0, 10):
                index += self.tableList[i * 10 + j]
                if itemRoom:
                    itemTable = itemRoom.child(j)
                    itemTable.setText(0,
                                      '桌子'.decode('utf-8') + str(j + 1) + '(' + str(self.tableList[i * 10 + j]) + '/2)')
            if itemRoom:
                itemRoom.setText(0, '房间'.decode('utf-8') + str(i + 1) + '(' + str(index) + '/20)')

    # 更新排行榜 只显示前三 不足前三时 有几个显示几个
    def rank(self):
        if self.scoreList:
            tmpcnt = 0
            newScoreList = sorted(self.scoreList.iteritems(), key=lambda d: d[1], reverse=True)
            # print newScoreList
            self.scoreListWigdet.clear()
            if len(newScoreList) >= 3:
                self.scoreListWigdet.addItem("第一名".decode('utf-8'))
                self.scoreListWigdet.addItem(newScoreList[0][0] + " : " + str(newScoreList[0][1]) + "分".decode('utf-8'))
                self.scoreListWigdet.addItem("第二名".decode('utf-8'))
                self.scoreListWigdet.addItem(newScoreList[1][0] + " : "
                                             + str(newScoreList[1][1]) + "分".decode('utf-8'))
                self.scoreListWigdet.addItem("第三名".decode('utf-8'))
                self.scoreListWigdet.addItem(newScoreList[2][0] + " : "
                                             + str(newScoreList[2][1]) + "分".decode('utf-8'))
            else:
                for slist in newScoreList:
                    tmpcnt += 1
                    self.scoreListWigdet.addItem("第".decode('utf-8') + str(tmpcnt) + "名".decode('utf-8'))
                    self.scoreListWigdet.addItem(slist[0] + " : " + str(slist[1]) + "分".decode('utf-8'))
            self.scoreListWigdet.update()
            tmpcnt = 0

    # 更新得分并显示
    def updateScore(self):
        if not self.userInfo.IsInRoom:
            self.scoreStatus1.setText("0 " + _fromUtf8("分"))
            self.scoreStatus2.setText("0 " + _fromUtf8("分"))
        else:
            if not self.userInfo.name.decode('utf-8') in self.scoreList.keys():
                self.scoreStatus1.setText("0 " + _fromUtf8("分"))
            else:
                self.scoreStatus1.setText(str(self.scoreList[self.userInfo.name.decode('utf-8')]) + _fromUtf8("分"))
            self.scoreStatus1.update()
            # 更新对手得分
            if  self.userInfo.opponent == None or ( not self.userInfo.opponent in self.scoreList.keys()):
                self.scoreStatus2.setText("0 " + _fromUtf8("分"))
            else:
                self.scoreStatus2.setText(str(self.scoreList[self.userInfo.opponent]) + _fromUtf8("分"))
            self.scoreStatus2.update()

    def GoingChess(self, data):
        self.infotext.setText(_fromUtf8("可以正式比赛了"))
        self.setButtonStatus(False, True, True, False, True, True)
        self.userInfo.IsBegin = True
        self.chessboard.mouseReleaseEvent = self.releaseAction
        # 如果白棋是自己的名字 那么自己的五子棋类型是白棋

        if data['white'] == self.userInfo.name.decode('utf-8'):
            self.infotext.setText(_fromUtf8('你是白棋，你后手'))
            self.userInfo.chessType = WHITE_CHESS
            self.userInfo.IsNext = False
            self.blackChess.setCheckable(False)
            self.whiteChess.setCheckable(True)
            self.userInfo.clearChessBoard()
            self.blackChess.setChecked(False)
            self.whiteChess.setChecked(True)
            self.blackChess.update()
            self.whiteChess.update()
        else:
            self.infotext.setText(_fromUtf8('你是黑棋，你先手'))
            self.userInfo.chessType = BLACK_CHESS
            self.userInfo.IsNext = True
            self.blackChess.setCheckable(True)
            self.whiteChess.setCheckable(False)
            self.blackChess.setChecked(True)
            self.whiteChess.setChecked(False)
            self.blackChess.update()
            self.whiteChess.update()

    def releaseAction(self, event):
        if event.button() == Qt.LeftButton:
            self.paint(event.pos().x(), event.pos().y())

    # 绘制棋子
    def paint(self, x, y):
        n, m = self.userInfo.leftMousePressEvent(x, y)
        if n != -1:
            data = {'sid': 100, 'cid': 1006, 'm': m, 'n': n, 'userlist': [self.userInfo.opponent], 'chesscnt': self.userInfo.chessCnt}
            self.ns.send(json.dumps(data))
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
        logging.debug("paint() userInfo.name: %s, chessCnt: %s" % (self.userInfo.name, self.userInfo.chessCnt))
        if self.userInfo.IsWhoWin(n, m):
            self.userInfo.IsNext = False
            self.setButtonStatus(False, False, False, False, True, True)
            self.infotext.setText(_fromUtf8('恭喜你赢了'))
            data = {'sid': 100, 'cid': 1007, 'winner': self.userInfo.name, 'loser': self.userInfo.opponent, 'chessType':
                self.userInfo.chessType}
            self.ns.send(json.dumps(data))
        elif n != -1 and self.userInfo.chessCnt >= 225:
            self.userInfo.IsNext = False
            self.setButtonStatus(False, False, False, False, True, True)
            self.infotext.setText(_fromUtf8('棋盘下满啦，和棋！'))
            self.userInfo.chessCnt = 0
            data = {'sid': 100, 'cid': 1010, 'userlist': [self.userInfo.opponent, self.userInfo.name]}
            self.ns.send(json.dumps(data))
        self.ns.process()

    # 发送广播信息
    def sendGroupMsgEvent(self):
        gtalkMsg = _toUtf8(self.groupChatEdit.text())
        gtalkMsg = str(gtalkMsg).strip()
        data = {'sid': 106, 'cid': 1001, 'message': gtalkMsg, 'user': self.userInfo.name}
        self.ns.send(json.dumps(data))
        self.ns.process()

    # 发送私聊信息
    def sendSingleMsgEvent(self):
        stalkMsg = _toUtf8(self.singleChatEdit.text())
        stalkMsg = str(stalkMsg).strip()
        if stalkMsg == '':
            return
        if self.userInfo.opponent == None:
            data = {'sid': 106, 'cid': 1003, 'message': stalkMsg,
                    'userlist': [self.userInfo.name], 'user': self.userInfo.name}
        else:
            data = {'sid': 106, 'cid': 1003, 'message': stalkMsg,
                    'userlist': [self.userInfo.opponent, self.userInfo.name], 'user': self.userInfo.name}
        # logging.debug("sendGroupMsgEvent data userlist() %s" % data['userlist'])
        self.ns.send(json.dumps(data))
        self.ns.process()

