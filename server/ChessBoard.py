# -*- coding: utf-8 -*-

import math, sip, logging


# 0代表没有棋子 1代表黑棋 2代表白棋
NO_CHESS = 0
BLACK_CHESS = 1
WHITE_CHESS = 2


class ChessBoard(object):

    def __init__(self, username, chessboard, infotext):

        self.IsInRoom = False   # 是否在房间里
        self.IsReady = False    # 是否准备好
        self.IsBegin = False    # 是否开始了
        self.IsLeave = False    # 是否离开了
        self.IsNext = False     # 对手是否可以下
        self.roomId = -1
        self.tableId = -1
        self.opponent = None
        self.IsNext = False
        self.chessType = NO_CHESS
        self.chessboard = chessboard
        self.name = username
        self.infotext = infotext
        self.gridWidth = 32
        self.limit = 5
        self.chessArray = [[(0, 0, NO_CHESS)] * 15 for i in range(0, 15)]
        self.chessStatus = [[(0, 0, NO_CHESS)] * 15 for i in range(0, 15)]
        self.path = []
        self.chessCnt = 0  # 判断棋子是否放满棋盘 如果放满 则自动判定为和棋

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
        if self.chessStatus[self.n][self.m][2] != NO_CHESS:
            return -1, -1
        self.IsNext = False
        self.chessCnt += 1
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
        self.chessArray = [[(0, 0, NO_CHESS)] * 15 for i in range(15)]
        self.chessStatus = [[(0, 0, NO_CHESS)] * 15 for i in range(15)]
        self.chessCnt = 0
        self.path = []


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

