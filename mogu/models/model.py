#coding=utf-8
#author:u'王健'
#Date: 13-6-1
#Time: 下午9:21
import json
import os
from tools.util import getImagesUrl

__author__ = u'王健'

from google.appengine.ext import db


class Users(db.Model):
    name = db.StringProperty()#本站昵称
    username = db.EmailProperty()
    password = db.StringProperty()
    auth = db.StringProperty()

#记录最新的用户名
class UserName(db.Model):
    userName = db.StringProperty()#用户名
    sessionid = db.StringProperty()#单点登录sessionid
    datetime = db.DateTimeProperty()#上次登录时间

class Game(db.Model):
    name = db.StringProperty(indexed=False)#游戏名称
    appcode = db.StringProperty()#游戏包名
    versioncode = db.IntegerProperty()#版本号
    versionname = db.StringProperty()#版本名称



class PropType(db.Model):
    game = db.StringProperty()#游戏
    name = db.StringProperty()#道具类型
    index = db.IntegerProperty()#索引

class Prop(db.Model):
    game = db.StringProperty()#游戏
    type = db.IntegerProperty()#道具类型
    name = db.StringProperty()#道具名称
    code = db.StringProperty()#道具识别码，根据道具识别码，来判断道具的作用
    codeid = db.StringProperty()#道具id,根据道具id判断道具种类（同样是炸弹、有些是赠送的、有些是花钱买的）
    desc = db.TextProperty()#介绍
    index = db.IntegerProperty()#索引

    # isgroup = db.BooleanProperty()#是否是某一种道具的打包套餐
    # groupcodeid = db.StringProperty()#道具打包套餐的id（道具套餐才起作用）
    # groupnum = db.IntegerProperty()#道具打包数量（道具套餐才起作用）

    # version = db.ListProperty(type=int)#支持游戏的版本
    ispub = db.BooleanProperty()#是否发布
    pricetype = db.IntegerProperty(indexed=False)#判断使用的价格类型（rmb 价格、游戏积分价格）
    price1 = db.IntegerProperty(indexed=False)#游戏积分价格
    price2 = db.IntegerProperty(indexed=False)#rmb价格
    images = db.ListProperty(item_type=int)#道具图片列表


class UserProp(db.Model):#用户所拥有的道具
    username = db.StringProperty()
    prop = db.StringProperty()
    num = db.IntegerProperty(indexed=False)
    game = db.StringProperty()

class UserPropBuy(db.Model):#用户购买道具的记录
    username = db.StringProperty()
    prop = db.StringProperty()
    num = db.IntegerProperty(indexed=False)
    game = db.StringProperty()
    datetime = db.DateTimeProperty()
    pricetype = db.IntegerProperty(indexed=False)#判断使用的价格类型（rmb 价格、游戏积分价格）
    price1 = db.IntegerProperty(indexed=False)#游戏积分价格
    price2 = db.IntegerProperty(indexed=False)#rmb价格

class UserPropUsed(db.Model):#用户使用道具的记录
    username = db.StringProperty()
    prop = db.StringProperty()
    num = db.IntegerProperty(indexed=False)
    game = db.StringProperty()
    datetime = db.DateTimeProperty()



class Images(db.Model):
    filename = db.StringProperty(indexed=False)
    filetype = db.StringProperty(indexed=False)
    size = db.IntegerProperty(indexed=False)
    data = db.BlobProperty()

    @property
    def id(self):
        return str(self.key().id())

    @property
    def imgurl(self):
        return getImagesUrl(self.key().id())


class Notice(db.Model):
    title = db.StringProperty(indexed=False)
    content = db.StringListProperty(indexed=False)
    type = db.IntegerProperty()
    plugin = db.IntegerProperty()
    pluginimg = db.IntegerProperty()
    lastUpdateTime = db.DateTimeProperty() #//最后一次修改时间
    startdate = db.DateTimeProperty(auto_now_add=True)  #//开始时间
    enddate = db.DateTimeProperty()  #//提交时间
    isdel = db.BooleanProperty(default=False)




