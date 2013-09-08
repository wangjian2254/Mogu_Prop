#coding=utf-8
#author:u'王健'
#Date: 13-9-7
#Time: 上午11:31
import json
import datetime
from google.appengine.ext import db
from mogu.models.model import Game, PropType, Prop, Images, UserProp, UserPropBuy, UserPropUsed
from tools.page import Page
from tools.util import getResult, getImagesUrl
timezone = datetime.timedelta(hours=8)
__author__ = u'王健'

def getGameList():
    return Game.all().order('appcode')

def getPropTypeList(game):
    return PropType.all().filter('game =',game).order('index')

def getPropList(game,type):
    list = Prop.all().filter('game =',game)
    if type:
        list = list.filter('type =',int(type))
    list = list.order('index')
    return list

def getUserPropList(username,game):
    return UserProp.all().filter('username =',username).filter('game =',game)

def getUserProp(username,propcodeid):
    for u in UserProp.all().filter('username =',username).filter('prop =',propcodeid):
        return u
    return None


class GetGameTypeList(Page):
    def get(self):
        game = self.request.get('game')
        list = getPropTypeList(game)
        l =[]
        for p in list:
            l.append({'id':p.key().id(), 'name':p.name})
        self.flush(json.dumps(l))

class ObjDelete(Page):
    def get(self,objname):
        id = self.request.get('id')
        if id:
            if objname == 'Game':
                obj = Game.get_by_id(int(id))
            elif objname == 'PropType':
                obj = PropType.get_by_id(int(id))
            elif objname == 'Prop':
                obj = Prop.get_by_id(int(id))
            elif objname == 'PropImage':
                pid = self.request.get('pid')
                obj = Images.get_by_id(int(id))
                prop = Prop.get_by_id(int(pid))
                prop.images.remove(int(id))
                prop.put()
            if obj:
                obj.delete()
                self.flush(getResult(id, True, u'删除成功。'))
                return
        self.flush(getResult('', False, u'删除失败，未提供id。'))

class ObjList(Page):
    def get(self,objname):
        list = []
        game = self.request.get('game')
        type = self.request.get('type')
        context={ 'game': game,'objname':objname}
        if objname == 'Game':
            list = getGameList()
        elif objname == 'PropType':
            glist = getGameList()
            list = getPropTypeList(game)
            context['gamelist']=glist
        elif objname == 'Prop':
            if not game and not type:
                glist = getGameList()
                context['gamelist']=glist
                self.render('template/prop/%sListGet.html'%objname, context)
                return
            list=getPropList(game,type)

        context['objlist']=list
        self.render('template/prop/%sList.html'%objname, context)


class GameUpdate(Page):
    def get(self):
        id = self.request.get('id', None)
        obj = {}
        if id:
            obj = Game.get_by_id(int(id))

        self.render('template/prop/gameUpdate.html', {'obj': obj, 'id': id})

    def post(self):
        id = self.request.get('id', None)
        name = self.request.get('name', None)
        # kind = self.request.get('kind', None)
        # kinds = []
        # if kind:
        #     kinds = kind.split()
        appcode = self.request.get('appcode', None)
        versioncode = self.request.get('versioncode', None)
        versionname = self.request.get('versionname', None)
        if id:
            obj = Game.get_by_id(int(id))
            msg = u'修改成功'
        else:
            obj = Game()
            msg = u'添加成功'

        obj.name = name
        # plugin.kinds = kinds
        obj.appcode = appcode
        obj.versioncode = int(versioncode)
        obj.versionname = versionname
        if not id and 0 < Game.all().filter('appcode =', appcode).count():
            self.render('template/prop/gameUpdate.html',
                        {'obj': obj, 'id': id, 'result': 'warning', 'msg': u'插件包名已经存在。'})
            return
        obj.put()
        self.render('template/prop/gameUpdate.html',
                    {'obj': obj, 'id': obj.key().id(), 'result': 'succeed', 'msg': msg})


class PropTypeUpdate(Page):
    def get(self):
        id = self.request.get('id', None)
        obj = {}
        if id:
            obj = PropType.get_by_id(int(id))
        gamelist = getGameList()

        self.render('template/prop/propTypeUpdate.html', {'obj': obj, 'id': id,'gamelist':gamelist})

    def post(self):
        id = self.request.get('id', None)
        name = self.request.get('name', None)
        game = self.request.get('game', None)
        index = self.request.get('index', None)
        if id:
            obj = PropType.get_by_id(int(id))
        else:
            obj = PropType()

        obj.name = name
        obj.game = game
        obj.index = int(index)

        obj.put()
        self.render('template/prop/propTypeUpdate.html',
                    {'obj': obj, 'id': obj.key().id(), 'result': 'succeed', 'msg': u'修改成功。'})


class PropUpdate(Page):
    def get(self):
        id = self.request.get('id', None)
        obj = {}
        if id:
            obj = Prop.get_by_id(int(id))
        gamelist = getGameList()

        self.render('template/prop/propUpdate.html', {'obj': obj, 'id': id,'gamelist':gamelist})

    def post(self):
        id = self.request.get('id', None)
        name = self.request.get('name', None)
        game = self.request.get('game', None)
        type = self.request.get('type', None)
        code = self.request.get('code', None)
        codeid = self.request.get('codeid', None)
        desc = self.request.get('desc', None)
        index = self.request.get('index', None)
        ispub = self.request.get('ispub', None)
        pricetype = self.request.get('pricetype', None)
        price1 = self.request.get('price1', None)
        price2 = self.request.get('price2', None)
        if id:
            obj = Prop.get_by_id(int(id))
        else:
            obj = Prop()

        obj.name = name
        obj.game = game
        obj.type = int(type)
        obj.code = code
        obj.codeid = codeid
        obj.desc = desc
        if ispub == '0':
            obj.ispub = False
        else:
            obj.ispub = True
        obj.pricetype = int(pricetype)
        if price1:
            obj.price1 = int(price1)
        else:
            obj.price1 = None
        if price2:
            obj.price2 = int(price2)
        else:
            obj.price2 = None
        obj.index = int(index)

        for i in range(1, 11):
            imgfilename = 'image' + str(i)
            imgfield = self.request.POST.get(imgfilename)
            if imgfield != '' and imgfield != u'' and imgfield != None:
                if imgfield.type.lower() not in ['image/pjpeg', 'image/x-png', 'image/jpeg', 'image/png', 'image/gif',
                                                 'image/jpg']:
                    continue
                imgfile = Images()
                imgfile.filename = imgfield.filename
                imgfile.filetype = imgfield.type
                imgfile.data = db.Blob(imgfield.file.read())
                imgfile.size = imgfield.bufsize
                imgfile.put()
                obj.images.append(imgfile.key().id())

        obj.put()
        gamelist = getGameList()
        self.render('template/prop/propUpdate.html',
                    {'obj': obj, 'id': obj.key().id(),'gamelist':gamelist,'game':game, 'result': 'succeed', 'msg': u'修改成功。'})

class ClientPropTypeList(Page):
    def get(self):
        game = self.request.get('game')
        if game:
            list=[]
            for p in getPropTypeList(game):
                list.append({'id':p.key().id(),'name':p.name,'game':p.game,'index':p.index})
            self.flush(getResult(list, True, u'获取道具类型成功。'))
            return
        self.flush(getResult('', False, u'获取道具类型，未提供id。'))


class ClientPropList(Page):
    def get(self):
        game = self.request.get('game')
        type = self.request.get('type')
        if game:
            list=[]
            content=None
            for p in getPropList(game,type):
                content={'id':p.key().id(),'name':p.name,'game':p.game,'type':p.type,'index':p.index,'code':p.code,'cod\
                eid':p.codeid,'desc':p.desc,'ispub':p.ispub,'pricetype':p.pricetype,'price1':p.price1,'price2':p.price2,'images':[]}
                for img in p.images:
                    content['images'].append({'id':img,'url':getImagesUrl(img)})
                list.append(content)
            self.flush(getResult(list, True, u'获取道具类型成功。'))
            return
        self.flush(getResult('', False, u'获取道具类型失败，未提供游戏code。'))

class ClientUserProp(Page):
    def get(self):
        username = self.request.get('username')
        game = self.request.get('game')
        if username and game:
            userproplist=getUserPropList(username,game)
            list = []
            for up in userproplist:
                list.append({'propcodeid':up.prop,'num':up.num,'game':up.game})
            self.flush(getResult(list, True, u'获取道具数量成功。'))
            return
        self.flush(getResult('', False, u'获取道具数量失败，参数不正确。'))

class ClientPropBuy(Page):
    def get(self):
        username = self.request.get('username')
        game = self.request.get('game')
        propcodeid = self.request.get('propcodeid')
        num = self.request.get('num')
        pricetype = self.request.get('pricetype')
        price1 = self.request.get('price1')
        price2 = self.request.get('price2')
        if username and game and propcodeid and num and pricetype :
            upb=UserPropBuy()
            upb.username = username
            upb.game = game
            upb.prop = propcodeid
            upb.num = int(num)
            upb.datetime = datetime.datetime.utcnow() + timezone
            upb.pricetype = int(pricetype)
            upb.price1 = int(price1)
            upb.price2 = int(price2)
            upb.put()
            uprop = getUserProp()
            if uprop:
                uprop.num=uprop.num+int(num)
                uprop.put()


            else:
                uprop=UserProp()
                uprop.username = username
                uprop.game = game
                uprop.prop = propcodeid
                uprop.num = int(num)
                uprop.put()
            self.flush(getResult('', True, u'购买道具成功。'))
            return
        self.flush(getResult('', False, u'购买道具失败，参数不正确。'))

class ClientPropUsed(Page):
    def get(self):
        username = self.request.get('username')
        game = self.request.get('game')
        propcodeid = self.request.get('propcodeid')
        num = self.request.get('num')

        if username and game and propcodeid and num  :
            upb=UserPropUsed()
            upb.username = username
            upb.game = game
            upb.prop = propcodeid
            upb.num = int(num)
            upb.datetime = datetime.datetime.utcnow() + timezone


            uprop = getUserProp()
            if uprop:
                if uprop.num>=int(num):
                    uprop.num=uprop.num-int(num)
                    uprop.put()
                    upb.put()
                    self.flush(getResult('', True, u'使用道具成功。'))
                    return
                else:
                    self.flush(getResult('', False, u'使用道具失败，道具数量不足。'))
                    return
            else:
                self.flush(getResult('', False, u'使用道具失败，道具数量不足。'))
                return
        self.flush(getResult('', False, u'使用道具失败，参数不正确。'))
