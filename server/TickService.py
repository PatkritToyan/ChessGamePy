# -*- coding:utf-8 -*-


class TickService(object):
    SERVICE_ID = 105

    def __init__(self):
        commands = {
            1001: self.tickResponse
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

    def tickResponse(self, msg):
        msg['sendType'] = 1
        return msg