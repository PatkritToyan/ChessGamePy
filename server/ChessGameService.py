# -*- coding:utf-8 -*-


class ChessGameService(object):

    SERVICE_ID = 104

    def __init__(self):
        commands = {
            1001: self.playAgainRequest,
            1002: self.playAgainResponse
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

    # 再来一局请求
    def playAgainRequest(self, msg):
        msg['sendType'] = 3
        return msg

    # 再来一局回应
    def playAgainResponse(self, msg):
        msg['sendType'] = 3
        return msg