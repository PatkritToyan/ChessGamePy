# -*- coding: utf-8 -*-

import locale
import sys
import math, sip, logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s




class ChessBoard(object):

    def __init__(self, username, chessboard, infotext):
        # 0代表没有棋子 1代表黑棋 2代表白棋
        self.NO_CHESS = 0
        self.BLACK_CHESS = 1
        self.WHITE_CHESS = 2
        self.IsInRoom = False   # 是否在房间里
        self.IsReady = False    # 是否准备好
        self.IsBegin = False    # 是否开始了
        self.IsLeave = False    # 是否离开了
        self.IsNext = False     # 对手是否可以下
        self.roomId = -1
        self.tableId = -1
        self.opponent = None
        self.IsNext = False
        self.chessType = self.NO_CHESS
        self.chessboard = chessboard
        self.name = username
        self.infotext = infotext
        self.gridWidth = 32
        self.limit = 5
        self.chessArray = [[(0, 0, self.NO_CHESS)] * 15 for i in range(0, 15)]
        self.chessStatus = [[(0, 0, self.NO_CHESS)] * 15 for i in range(0, 15)]
        self.path = []

    # 计算棋子放置的坐标 根据鼠标位置确定绘制的是哪一个格子
    def chessLos(self, xLos, yLos):
        n = int(math.floor((xLos - 5) / self.gridWidth))
        m = int(math.floor((yLos - 5) / self.gridWidth))
        if n <= 0:
            n = 0
        elif n > 14:
            n = 14
        if m <= 0:
            m = 0
        elif m > 14:
            m = 14
        return n, m, self.gridWidth * n + 5, self.gridWidth * m + 5

    # 绘制当前棋子
    def leftMousePressEvent(self, curX, curY):
        if not self.IsBegin:
            return -1, -1
        if not self.IsNext:
            return -1, -1

        self.n, self.m, self.x, self.y = self.chessLos(curX, curY)

        # 如果棋盘上有棋，就不能下
        if self.chessStatus[self.n][self.m][2] != self.NO_CHESS:
            return -1, -1
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
        logging.debug("leftMousePressEvent() n: %s, m: %s " % (self.n, self.m))
        # 绘制棋子
        self.chessStatus[self.n][self.m] = (self.x, self.y, self.chessType)
        self.path.append([self.n, self.m])
        self.chessArray[self.n][self.m] = QGraphicsView(self.chessboard)
        self.chessArray[self.n][self.m].setGeometry(QRect(32 * self.n, 32 * self.m, 32, 32))
        if self.chessType == self.BLACK_CHESS:
            self.chessArray[self.n][self.m].setStyleSheet(_fromUtf8("background-image:url(:images/blackchess.png)"))
        elif self.chessType == self.WHITE_CHESS:
            self.chessArray[self.n][self.m].setStyleSheet(_fromUtf8("background-image:url(:images/whitechess.png)"))
        self.chessArray[self.n][self.m].setFrameShape(QFrame.NoFrame)
        self.chessArray[self.n][self.m].show()
        self.IsNext = False
        self.infotext.setText("我下完了，到您了".decode('utf-8'))
        self.chessboard.update()
        return self.n, self.m

    # 清楚棋盘数据
    def clearChessBoard(self):
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
        logging.debug("clearChessBoard() chessArray[][]: %s " % self.chessArray)
        # 清除原有棋子
        for i in range(len(self.path)):
            n = self.path[-1][0]
            m = self.path[-1][1]
            self.path.pop()
            self.chessStatus[n][m] = (float(self.x), float(self.y), 0)
            if self.chessArray[n][m] != None:
                sip.delete(self.chessArray[n][m])
                self.chessArray[n][m] = None
            self.chessboard.update()
        # 重新初始化数据
        self.chessArray = [[(0, 0, self.NO_CHESS)] * 15 for i in range(15)]
        self.chessStatus = [[(0, 0, self.NO_CHESS)] * 15 for i in range(15)]
        self.path = []

    # 更新棋盘
    def updateChessBoard(self, n, m):
        oppo = self.WHITE_CHESS
        if self.chessType == self.WHITE_CHESS:
            oppo = self.BLACK_CHESS

        x = float(n * self.gridWidth + self.limit)
        y = float(m * self.gridWidth + self.limit)
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
        logging.debug("updateChessBoard() x: %s, y: %s " %  (x , y))
        # 绘制当前棋子
        self.chessArray[n][m] = (x, y, oppo)
        self.path.append([n, m])
        self.chessArray[n][m] = QGraphicsView(self.chessboard)
        self.chessArray[n][m].setGeometry(QRect(32 * n, 32 * m, 32, 32))
        if oppo == self.BLACK_CHESS:
            self.chessArray[n][m].setStyleSheet(_fromUtf8("background-image: url(:images/blackchess.png);"))
        else:
            self.chessArray[n][m].setStyleSheet(_fromUtf8("background-image: url(:images/whitechess.png);"))
        self.chessArray[n][m].setFrameShape(QFrame.NoFrame)
        self.chessArray[n][m].show()
        self.IsNext = True
        self.infotext.setText(_fromUtf8("我方下"))
        self.chessboard.update()

    # 判断当前输赢
    def IsWhoWin(self, x, y):
        # 计算水平方向
        i = x
        j = y
        cnt = 0
        while i >= 0 and self.chessStatus[i][j][2] == self.chessType:
            i -= 1
            cnt += 1
        i = x + 1
        while i <= 14 and self.chessStatus[i][j][2] == self.chessType:
            i += 1
            cnt += 1
        if cnt >= 5:
            return True
        # 计算竖直方向
        i = x
        j = y
        cnt = 0
        while j >= 0 and self.chessStatus[i][j][2] == self.chessType:
            cnt += 1
            j -= 1
        j = y + 1
        while j <= 14 and self.chessStatus[i][j][2] == self.chessType:
            j += 1
            cnt += 1
        if cnt >= 5:
            return True
        # 计算135°方向
        i = x
        j = y
        cnt = 0
        while i >= 0 and j >= 0 and self.chessStatus[i][j][2] == self.chessType:
            i -= 1
            j -= 1
            cnt += 1
        i = x + 1
        j = y + 1
        while i <= 14 and j <= 14 and self.chessStatus[i][j][2] == self.chessType:
            i += 1
            j += 1
            cnt += 1
        if cnt >= 5:
            return True
        # 计算机45°方向
        i = x
        j = y
        cnt = 0
        while i >= 0 and j <= 14 and self.chessStatus[i][j][2] == self.chessType:
            i -= 1
            j += 1
            cnt += 1
        i = x + 1
        j = y - 1
        while i <= 14 and j >= 0 and self.chessStatus[i][j][2] == self.chessType:
            i += 1
            j -= 1
            cnt += 1
        if cnt >= 5:
            return True
        return False

