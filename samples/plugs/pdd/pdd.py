import configparser
import os
import uuid
import fnmatch
import itchat
import requests
import json
import random
import shutil
from time import strftime
import time
from configparser import RawConfigParser
from wxpusher import WxPusher

"""
拼多多推广自动化2020.11.9
"""


class Pdd:
    goods = []
    goods_stack = []
    goodsinfo = {}
    headers = {}

    def __init__(self):
        config = configparser.RawConfigParser()
        config.read(r'C:\Users\index\PycharmProjects\wechat_pc_api\samples\plugs\pdd\config.ini')
        cookie = config.get('app', 'cookie')
        goodsinfo = {'goodId', 'mallId', 'zsid'}
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'cookie': cookie,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        }

    # data = {
    #     'keyWord': '',
    #     'pageNumber': 1,
    #     'pageSize': 200,
    #     'sectionId': '',
    #     'sectionName': '/promotion/daily-promotion'
    # }

    def searchGoods(self, key):
        #生成随机索引
        Upper=random.randint(3, 60)
        self.goodsinfo.clear()
        self.goods.clear()
        data = {
            'categoryId': -1,
            'keyword': key,
            'pageNumber': 1,
            'pageSize': 60
        }
        res_post = requests.post(url="https://jinbao.pinduoduo.com/network/api/common/goodsList",
                                 data=json.dumps(data), headers=self.headers)
        res_post = json.loads(res_post.content)
        preparedata = res_post['result']['goodsList']
        print(preparedata)
        for i in range(Upper-3,Upper):
            self.goodsinfo['goodId'] = preparedata[i]['goodsId']
            self.goodsinfo['mallId'] = preparedata[i]['mallId']
            self.goods.append(self.goodsinfo.copy())
        print(self.goods.__len__())
        return self.goods
    # 获取商品id列表
    def getgoodsIds(self, page):
        data2 = {
            'activityId': 27,
            'goodsNum': 20
        }
        data3 = {
            'listId': 'null',
            'pageNumber': page,
            'pageSize': 40,
            'sortType': 2,
            'type': 1,
        }
        data4 = {

        }
        # res_post = requests.post(url="https://jinbao.pinduoduo.com/network/api/activity/extraGoods",
        #                          data=json.dumps(pdd.data2), headers=self.headers)

        res_post = requests.post(url="https://jinbao.pinduoduo.com/network/api/common/queryTopGoodsList",
                                 data=json.dumps(data3), headers=self.headers)
        res_post = json.loads(res_post.content)
        preparedata = res_post['result']['list']
        # res_post = requests.post(url="https://jinbao.pinduoduo.com/network/api/common/goods/dailyPush",
        #                          data=json.dumps(data4),headers=self.headers)
        # res_post = json.loads(res_post.content)
        # preparedata = res_post['result']['goodsList']
        for good in preparedata:
            self.goodsinfo['goodId'] = (good['goodsId'])
            self.goodsinfo['mallId'] = (good['mallId'])
            self.goods.append(self.goodsinfo.copy())
        return self.goods

    # 填充招商szid
    def getszid(self, ids):
        self.goods_stack.clear()
        for id in ids:
            data4 = {
                'goodsId': id['goodId'],
                'mallId': id['mallId'],
                'sectionId': '',
                'sectionName': ''
            }
            res_post = requests.post(url='https://jinbao.pinduoduo.com/network/api/common/goods/promotionUnits',
                                     data=json.dumps(data4), headers=self.headers)
            res_post = json.loads(res_post.content)
            if res_post['result']['list'][0]['zsDuoId']:
                zsDuoId = res_post['result']['list'][0]['zsDuoId']
                self.goodsinfo['mallId'] = id['mallId']
                self.goodsinfo['goodId'] = id['goodId']
                self.goodsinfo['zsid'] = zsDuoId
                self.goods_stack.append(self.goodsinfo.copy())
            else:
                self.goodsinfo['mallId'] = id['mallId']
                self.goodsinfo['goodId'] = id['goodId']
                self.goodsinfo['zsid'] = 0
                self.goods_stack.append(self.goodsinfo.copy())

        return self.goods_stack

    # 获取推广链接
    def getCreateImg(self, szids):
        imglist = []
        for Id in szids:
            goodsId = Id['goodId']
            zsDuoId = Id['zsid']
            data_img = {
                'goodsId': goodsId,
                'multiGroup': 'false',
                'pid': '13774022_179622014',
                'sectionId': '',
                'sectionName': '/promotion/daily-promotion',
                'type': 0,
                'zsDuoId': zsDuoId
            }
            res_post = requests.post(url="https://jinbao.pinduoduo.com/network/api/promotion/createPromotionImage",
                                     data=json.dumps(data_img), headers=self.headers)
            res_post = json.loads(res_post.content)
            # print(res_post['result']['list'])
            imglist.append(res_post['result'])
        print('imglist')
        print(imglist)
        return imglist.copy()

    def getCookiesBySMS(self):
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Host': 'jinbao.pinduoduo.com',
            'Connection': 'keep-alive',
            'origin': 'https://jinbao.pinduoduo.com',

            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same - origin',
        }
        data = {
            'mobile': '17691162035',
        }
        res_post = requests.post(url='https://jinbao.pinduoduo.com/network/api/common/createMessageToken',
                                 data=json.dumps(data), headers=headers)
        res_post = json.loads(res_post.content)
        print(res_post['result'])
        token = res_post['result']

        data_code = {
            'mobile': '17691162034',
            'version': 2,
            'token': str(token),
            'router': 1,
        }
        res_post = requests.post(url='https://jinbao.pinduoduo.com/network/api/common/createMessageCode',
                                 data=json.dumps(data_code), headers=headers)
        print(res_post.content)

    def downloadpic(self, url):
        img = requests.get(url)
        filename = time.strftime("%Y-%m-%d", time.localtime()) + "-" + str(uuid.uuid4())
        path = "./img"
        if not os.path.exists(path):
            os.makedirs(path)
        with open("./img/{}.jpg".format(filename), 'wb') as f:
            f.write(img.content)
            print("下载图片...")
        print("下载完毕")
        return "./img/" + filename + ".jpg"

    def getimgnamelist(self):
        imgresoureslist = []
        for f_name in os.listdir('./img'):
            if fnmatch.fnmatch(f_name, '*.jpg'):
                imgresoureslist.append(f_name)
        return imgresoureslist

    # AT_LJCaq35NcYeliZLP4SNVNdPLWTRIHFzT
    def severJiang(self, urls):
        # filename = time.strftime("%Y-%m-%d", time.localtime())
        title = "拼多多-内购通知-"
        print(title)
        # server
        url0 = 'http://push.ijingniu.cn/send?key=e429ec8a0d1345efb235c6ba667b8577'
        # 账号1
        serverURL = "https://sc.ftqq.com/SCU88343Td759ddfc7669be102e9d9bdd14796d7f5e6382ff83b3a.send"  # 替换为自己的key值
        # 账号2
        serverURL2 = "https://sc.ftqq.com/SCU125363Tdaaca1f34e4b43d74a03d746ae62777b5faa76f6e2b7b.send"  # 替换为自己的key值
        strings = ''
        for url in urls:
            strings += '![avatar](' + url + ')'
        print(strings)
        # params = {
        #     'head': title,
        #     'body': str(strings)
        # }
        res = requests.session().get(url0 + '&head=' + title + '+&body=' + strings)
        print(res.content)
        # requests.session().post(serverURL, data=params)
        # requests.session().post(serverURL2, data=params)

    def sendMessages(self, msg):
        date = time.strftime("%Y-%m-%d", time.localtime())
        msgs = '<font  color=gray size=5>内购券汇总-下滑更多👇</font>\n'
        for url in msg:
            msgs += '![avatar](' + url + ')\n' + '<hr>\n'
        print(msgs)
        print(WxPusher.query_user('1', '10', 'AT_LJCaq35NcYeliZLP4SNVNdPLWTRIHFzT'))
        res = WxPusher.send_message(msgs,
                                    uids=[],
                                    topic_ids=[1000],
                                    token='AT_LJCaq35NcYeliZLP4SNVNdPLWTRIHFzT',
                                    content_type=3,
                                    summary='发券通知💌\n时间: ' + date + '👇')
        print(res)


if __name__ == '__main__':
    # 加载配置文件读取cookie 初始化数据
    pdd = Pdd()
    # 微信登录
    # itchat.auto_login(hotReload=True,enableCmdQR=2)
    # pdd.getCookiesBySMS()
    ids = pdd.getgoodsIds(page=1)
    print(ids)
    zsids = pdd.getszid(ids)
    print(zsids)
    imglist = pdd.getCreateImg(zsids)
    # pdd.sendMessages(imglist)
    # pdd.severJiang(imglist)
    # 下载图片
    # for img in imglist:
    # pdd.downloadpic(img)
    # 用于接收群里面的对话消息
    # @itchat.msg_register([itchat.content.TEXT], isGroupChat=True)
    # def print_content(msg):
    #     # message:取出msg里面的文本消息
    #     replay=''
    #     message = msg['Text']
    #     if u'召唤神龙' in message:
    #         replay = u'测试通过--:o'
    #     if u'@优惠券'in message:
    #         chat_rooms = itchat.search_chatrooms(name='多多特价券')
    #         if len(chat_rooms) > 0:
    # itchat.send_msg('测试', chat_rooms[0]['UserName'])
    # itchat.send_image(fileDir='', toUserName=chat_rooms[0]['UserName'])
    #     return replay

    #
    # imgNameList = pdd.getimgnamelist()
    # chat_rooms = itchat.search_chatrooms(name='多多内部券')
    # print("-------------开始推送-----------")
    # if len(chat_rooms) > 0:
    #     for img in imgNameList:
    #         img = './img/' + img
    #         print(img + "已发送")
    #         itchat.send_image(fileDir=img, toUserName=chat_rooms[0]['UserName'])
    #         time.sleep(5)
    # shutil.rmtree("./img")
    # itchat.run()
