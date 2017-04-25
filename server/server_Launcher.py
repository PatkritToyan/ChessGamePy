# -*- coding: utf-8 -*-

import json, logging
from netstream import *
from dispatcher import *
from TableShowService import *
from ChessGameService import *
from ChatService import *
from TickService import *


class Server_Launcher(object):

    def __init__(self):
        self.host = nethost(8)
        self.host.startup(2000)
        print('service startup at port', self.host.port)
        self.host.settimer(2000)
        self.userList = {}


if __name__ == '__main__':

    # 任务处理分发器
    dispatch = dispatcher()
    # 注册各类服务
    dispatch.register(TableShowService.SERVICE_ID, TableShowService())
    dispatch.register(ChessGameService.SERVICE_ID, ChessGameService())
    dispatch.register(ChatService.SERVICE_ID, ChatService())
    dispatch.register(TickService.SERVICE_ID, TickService())

    server = Server_Launcher()
    while True:
        server.host.process()
        event, wparam, lparam, data = server.host.read()

        if event < 0:
            continue
        # 处理玩家数据
        if event == NET_DATA:
            data = json.loads(data)
            logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
            logging.debug("Server_Launcher() NET_DATA data: %s, wparam:%s" % (data, wparam))
            # 第一次登录进来 记录用户人
            if data['sid'] == 103:
                server.userList[data['user']] = wparam
            else:
                result = dispatch.dispatch(data)
                logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
                logging.debug("Server_Launcher() result: %s " % result)
                logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
                logging.debug("Server_Launcher() userList: %s " % server.userList)
                # 将服务端处理完的数据返回给发送者
                if result['sendType'] == 1:
                    server.host.send(wparam, json.dumps(result))
                # 将服务端处理完的数据返回给所有人
                elif result['sendType'] == 2:
                    for user in server.userList.keys():
                        server.host.send(server.userList[user], json.dumps(result))
                # 将服务端处理完的数据返回给 部分人
                elif result['sendType'] == 3:
                    if result['userlist']:
                        for user in result['userlist']:
                            server.host.send(server.userList[user], json.dumps(result))
                server.host.process()
            if data == 'exit':
                print 'client request to exit'
                server.host.close()
        # 处理玩家进入
        elif event == NET_NEW:
            logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
            logging.debug("Server_Launcher() NET_NEW data: %s, wparam:%s" % (data, wparam))
            print wparam, 'is in'
            # sid == 101表示登录成功
            data = {'sid': 101, 'type': 'HELLO CLIENT %X' % wparam}
            server.host.send(wparam, json.dumps(data))
            server.host.settag(wparam, wparam)
            server.host.nodelay(wparam, 1)
        # 处理时钟
        elif event == NET_TIMER:
            logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
            logging.debug("Server_Launcher() NET_TIMER data: %s" % data)
            # 发送桌子列表
            data = {'sid': 100, 'cid': 1001}
            result = dispatch.dispatch(data)
            for user in server.userList.keys():
                server.host.send(server.userList[user], json.dumps(result))
        # 处理玩家离开
        elif event == NET_LEAVE:
            logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
            logging.debug("Server_Launcher() NET_TIMER wparam: %s" % wparam)
            print wparam, 'is out'
            server.host.close(wparam)
