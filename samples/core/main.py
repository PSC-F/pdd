# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import shutil
import wechat
import json
import time
from wechat import WeChatManager, MessageType
import requests
from samples.plugs.pdd.pdd import Pdd
wechat_manager = WeChatManager(libs_path='../../libs')


# 这里测试函数回调
@wechat.CONNECT_CALLBACK(in_class=False)
def on_connect(client_id):
    print('[on_connect] client_id: {0}'.format(client_id))


# 增强发送消息逻辑
def sendMessage(client_id, message_data,messages):
    """
    :param client_id: 客户端Id-自动生成
    :param message_data: 收到的原始消息内容
    :param messages: 回复的消息内容
    :return:
    """
    if message_data['room_wxid']:  # 回复-暗号来自群聊的消息
        wechat_manager.send_text(client_id, message_data['room_wxid'], messages)
    elif message_data['from_wxid']:  # 回复-暗号来自个人的消息
        # wechat_manager.send_link(client_id, message_data['from_wxid'], url="http://baidu.com", title="百度" ,desc="百度一下",image_url='https://img-home.csdnimg.cn/images/20201103102506.gif')
        wechat_manager.send_text(client_id, message_data['from_wxid'], messages)
# 增强发送图片逻辑
def sendImage(client_id, message_data,imglistDir):
    """
    :param client_id: 客户端Id-自动生成
    :param message_data: 收到的原始消息内容
    :param messages: 回复的消息内容
    :return:
    """
    pre='C://Users//index//PycharmProjects//wechat_pc_api//samples//core//img//'
    if message_data['room_wxid']:  # 回复-暗号来自群聊的图片
        for imgdir in imglistDir:
            print("最终路径" + pre + imgdir)
            wechat_manager.send_image(client_id,
                                      message_data['room_wxid'],
                                      wechat_manager.send_image(client_id,message_data['room_wxid'],pre+imgdir))
            time.sleep(2)
    elif message_data['from_wxid']:  # 回复-暗号来自个人的图片
        for imgdir in imglistDir:
            time.sleep(3)
            print("最终路径" + pre + imgdir)
            wechat_manager.send_image(client_id,
                                      message_data['from_wxid'],
                                      wechat_manager.send_image(client_id,message_data['from_wxid'], pre+imgdir))
        #删除
    shutil.rmtree("C://Users//index//PycharmProjects//wechat_pc_api//samples//core//img//")
    # shutil.rmtree("./img")
def enableDefaultKey(keyWords,message_data,client_id):
    if keyWords in message_data['msg']:
        messages = requests.get(url='http://hzct.net/api/saohua/api.php')
        sendMessage(client_id, message_data, messages.text)
def enableShoppingKey(keyWords,message_data,client_id):
    if keyWords in message_data['msg']:
        # 过滤查询参数
        param=str(message_data['msg']).split('拼多多', 1)[1]
        print("查询模式----<查询参数>:"+param)
        sendImage(client_id, message_data, getimglistByPdd(param))

def enableWealthinKey(keyWords, message_data, client_id):
            if keyWords in message_data['msg']:
                messages = requests.get(url='http://api.help.bj.cn/apis/weather/?id=101060101')
                print(messages.content)
                # message='时间:'+messages['today']+'温度:'+messages['temp']+"雾霾"+messages['aqi']
                sendMessage(client_id, message_data, messages.content)
def intellgentBotKey(keyWords, message_data, client_id):
    # if keyWords in message_data['msg']:
        messages = requests.get(url='http://api.qingyunke.com/api.php?key=free&appid=0&msg='+message_data['msg'])
        res = json.loads(messages.text)
        sendMessage(client_id, message_data, res['content'])

def getimglistByPdd(keyWords):
    """
    获取图片路径
    :return:
    """
    print("调用PDD插件")
    pdd = Pdd()
    # ids = pdd.getgoodsIds(page=1)
    ids = pdd.searchGoods(keyWords)
    zsids = pdd.getszid(ids)
    imglist = pdd.getCreateImg(zsids)
    print("图片URL列表:")
    print(imglist)
    #下载图片
    for img in imglist:
        pdd.downloadpic(img)
    imgNameList = pdd.getimgnamelist()
    print("获取下载地址路径")
    print(imgNameList)
    return imgNameList
@wechat.RECV_CALLBACK(in_class=False)
def on_recv(client_id, message_type, message_data):
    # print('[on_recv] client_id: {0}, message_type: {1}, message:{2}'.format(client_id,
    #                                                          message_type, json.dumps(message_data)))
    print(message_data)
    if message_type == MessageType.MT_RECV_TEXT_MSG:
        if 'intellj_push' in message_data['at_user_list']:
            if '暗号' in message_data['msg']:
                enableDefaultKey("暗号",message_data,client_id)
            elif '拼多多' in message_data['msg']:
                enableShoppingKey("拼多多",message_data,client_id)
            else:
                intellgentBotKey("菲菲",message_data,client_id)
            # enableWealthinKey("天气",message_data,client_id)
        elif message_data['is_pc']==0 and message_data['room_wxid']=='':
            intellgentBotKey("菲菲", message_data, client_id)
            enableDefaultKey("暗号", message_data, client_id)

@wechat.CLOSE_CALLBACK(in_class=False)
def on_close(client_id):
    print('[on_close] client_id: {0}'.format(client_id))


# 这里测试类回调， 函数回调与类回调可以混合使用
class LoginTipBot(wechat.CallbackHandler):

    @wechat.RECV_CALLBACK(in_class=True)
    def on_message(self, client_id, message_type, message_data):
        # 判断登录成功后，就向文件助手发条消息
        if message_type == MessageType.MT_USER_LOGIN:
            time.sleep(2)
            wechat_manager.send_text(client_id, 'filehelper', '😂😂😂')

            # wechat_manager.send_link(client_id,
            # 'filehelper',
            # 'wechat_pc_api项目',
            # 'WeChatPc机器人项目',
            # 'https://github.com/smallevilbeast/wechat_pc_api',
            # 'https://www.showdoc.com.cn/server/api/attachment/visitfile/sign/0203e82433363e5ff9c6aa88aa9f1bbe?showdoc=.jpg)')


if __name__ == "__main__":
    bot = LoginTipBot()

    # 添加回调实例对象
    wechat_manager.add_callback_handler(bot)
    wechat_manager.manager_wechat(smart=True)
    # 阻塞主线程
    while True:
        time.sleep(0.5)
