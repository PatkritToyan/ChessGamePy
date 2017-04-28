# 网络五子棋
####Introduction
*  使用 netstream.py
*  客户端：netstream
*  服务器：nethost
*  消息协议：json

* ClientLogin_Launcher.py 为客户端登录启动程序
* UI_ChessGame.ui 为房间和下棋Ui
* UI_ChessGame.py 为房间和下棋UI对应的py文件
* ClientLogin.ui 为用户登录ui
* ClientLogin.py 为用户登录ui对应的py文件
* generote_icon.py 为将images.qrc转化为images.py的脚本
* ChessGame.py 为客户端逻辑文件
* $$ server文件  $$
* netstream.py为网络通信底层文件
* dispatcher.py为相应的服务转发代码
* ChatService.py 为房间聊天和大厅聊天的服务
* ChessGameService.py 为再玩一次 以及和棋的服务
* TableShowService.py 为 玩家进入 玩家离开 准备 获取得分等诸多服务
* server_Launcher.py 为服务器启动程序
* TickService.py 为心跳服务

####Features:
* 实现输入服务器IP和端口及昵称登录
* 实现桌子列表
* 选择桌子坐下
* 大厅里面聊天
* 五子棋落子消息
* 判断输赢和结果显示
* 房间里面聊天
* 实现排行榜
* 支持中文登录和显示
* 实现胜平负积分

####TODO:
* 实现竞手.
* 实现悔棋
* 实现数据存储（仅存储历史用户列表和得分记录）

####How To Running:
* 先启动 server/server_Launcher.py
* 然后启动 ClientLogin_Launcher.py
* 输入ip地址 127.0.0.1
* 默认监听端口 9999
* 点开房间列表
* 选择其中一张桌子
* 进入房间后 如果满2人 都准备 即可开始比赛
* 胜者得3分 负者得-1分 平手0分