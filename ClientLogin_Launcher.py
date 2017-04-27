# -*- coding: utf-8 -*-

import json, sys, socket, logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ClientLogin import *
from server import netstream
from ChessGame import *
from server import netstream

try:
    _toUtf8 = QString.toUtf8
except AttributeError:
    def _toUtf8(s):
        return s

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class ClientLogin_launcher(QWidget, Ui_Dialog):

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        self.connect(self.miniBt, SIGNAL("clicked()"), self.showMinimized)
        self.connect(self.closeBt, SIGNAL("clicked()"), self.hide)
        self.connect(self.loginBt, SIGNAL("clicked()"), self.login)

    def is_valid_ip(self, ip):
        """Returns true if the given string is a well-formed IP address. 

            Supports IPv4 and IPv6. 
            """
        if not ip or '\x00' in ip:
            # getaddrinfo resolves empty strings to localhost, and truncates
            # on zero bytes.
            return False
        try:
            res = socket.getaddrinfo(ip, 0, socket.AF_UNSPEC,
                                     socket.SOCK_STREAM,
                                     0, socket.AI_NUMERICHOST)
            return bool(res)
        except socket.gaierror as e:
            if e.args[0] == socket.EAI_NONAME:
                return False
            raise
        return True

    def login(self):
        self.username = str(_toUtf8(self.username_val.text())).strip()
        if self.username == "":
            QMessageBox.warning(self, _fromUtf8("警告"), _fromUtf8("昵称不能为空!"), QMessageBox.Yes)
        self.ip = str(self.ip_val.text()).strip()
        if not self.is_valid_ip(self.ip):
            QMessageBox.warning(self, _fromUtf8("警告"), _fromUtf8("请输入合法的ip地址!"), QMessageBox.Yes)
        self.port = int(self.port_val.text())
        self.ns = netstream.netstream(8)
        self.ns.connect(self.ip, self.port)

        self.timer = QTimer()
        self.timer.timeout.connect(self.serverConnection)
        self.timer.start(100)

    def loginSuccess(self):
        self.close()
        self.timer.stop()
        self.client = ChessGame(self.ip, self.port, self.username, self.ns)
        self.client.connectToServer()
        self.client.show()

    def loginError(self):
        QMessageBox.information(self, _fromUtf8('提示'),_fromUtf8("登录失败!"))

    # 连接服务器
    def serverConnection(self):
        self.ns.process()
        if self.ns.status() == netstream.NET_STATE_ESTABLISHED:
            data = self.ns.recv()
            logging.basicConfig(level=logging.DEBUG, format='[%(asctime)s] %(name)s:%(levelname)s: %(message)s')
            logging.debug(" serverConnection data() x: %s" % data)
            print 'serverconnection'
            if len(data) > 0:
                # 约定协议为json格式
                data = json.loads(data)
                if data['sid'] == 101:
                    print '101'
                    message = {'sid': 103, 'user': self.username}
                    self.ns.send(json.dumps(message))
                    self.ns.process()
                elif data['sid'] == 120:
                    print '120'
                    if data['reply'] == 'error':
                        QMessageBox.information(self, _fromUtf8('提示'), _fromUtf8("用户名冲突，请更换用户名！"))
                    else:
                        print 'login success'
                        self.loginSuccess()
                else:
                    self.loginError()


class MyApplication(QApplication):

    def __init__(self, args):
        super(MyApplication, self).__init__(args)

    def GET_X_LPARAM(self, param):
        return param & 0xffff

    def GET_Y_LPARAM(self, param):
        return param >> 16

    def winEventFilter(self, msg):
        if msg.message == 0x84:
            form = self.activeWindow()
            if form:
                xPos = self.GET_X_LPARAM(msg.lParam) - form.frameGeometry().x()
                yPos = self.GET_Y_LPARAM(msg.lParam) - form.frameGeometry().y()
                self.desktop = QDesktopWidget()
                self.desktopSize = QDesktopWidget.availableGeometry(self.desktop).size()
                if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isTopLeft')\
                        and form.isTopLeft(xPos, yPos):
                    return True, 0xD
                if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isTopRight')\
                        and form.isTopRight(xPos, yPos):
                    return True, 0xE
                if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isBottomLeft')\
                        and form.isBottomLeft(xPos, yPos):
                    return True, 0x10
                if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isBottomRight')\
                        and form.isBottomRight(xPos, yPos):
                    return True, 0x11
                if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isLeft') and\
                        form.isLeft(xPos):
                    return True, 0xA
                if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isRight') and \
                        form.isRight(xPos):
                    return True, 0xB
                if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isTop') and \
                        form.isTop(yPos):
                    return True, 0xC
                if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isBottom') and \
                        form.isBottom(yPos):
                    return True, 0xF
                if not form.isFullScreen() and self.desktopSize != form.size() and hasattr(form, 'isInTitle') and \
                        form.isInTitle(xPos, yPos):
                    return True, 0x2

        elif msg.message == 0xA3:
            pass
        return False, 0



if __name__ == "__main__":
    app = MyApplication(sys.argv)
    loginForm = ClientLogin_launcher()
    loginForm.show()
    sys.exit(app.exec_())