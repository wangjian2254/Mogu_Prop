#coding=utf-8
#author:u'王健'
#Date: 13-9-7
#Time: 上午11:31
import json
from google.appengine.ext import db
from mogu.models.model import Game, PropType, Prop, Images
from tools.page import Page
from tools.util import getResult

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

