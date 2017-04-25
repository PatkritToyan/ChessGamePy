# -*- coding:utf-8 -*-
import logging

class ChatService(object):

    SERVICE_ID = 106

    def __init__(self):
        commands = {
            1001: self.groupChat,
            1003: self.singleChat,
        }
        self.registers(commands)

    def handle(self, msg):
        cid = msg['cid']
        if not cid in self.__command_map:
            raise Exception('bad command %s'%cid)
        f = self.__command_map[cid]
        return f(msg)

    def register(self, cid, function):
        self.__command_map[cid] =  function

    def registers(self, CommandDict):
        self.__command_map = {}
        for cid in CommandDict:
            self.register(cid, CommandDict[cid])
        return 0

    # 群聊
    def groupChat(self, msg):
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
        logging.debug("groupChat SERVICE msg:%s" % msg)
        msg['sendType'] = 2
        return msg

    # 单聊
    def singleChat(self, msg):
        logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
        logging.debug("singleChat SERVICE msg:%s" % msg)
        msg['sendType'] = 3
        return msg