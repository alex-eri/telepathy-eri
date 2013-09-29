from utils.decorators import loggit

__author__ = 'eri'
import vkcom.api
import threading
import httplib
import urllib
import time
import signal
try:
    import simplejson as json
except ImportError:
    import json

CLIENT_ID = '3827733'
CLIENT_SCOPE = 'friends,messages,offline'
CLIENT_SECRET = None
WAIT = 28
MODE = 2

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Vk.Messenger')
import os

class ContactList(object):
    def __init__(self,Api,fields='screen_name,photo_50',items=()):
        self.getter = Api
        self.cl = {}
        self.fields  = fields
        for i in items:
            uid = i.get('id')
            if uid:
                self.cl[str(uid)] = i

    @loggit(logger)
    def __getitem__(self, item):
        #TODO accept only valid ids
        # item = str(item).strip()
        uid = str(item).strip()
        contact = self.cl.get(item)
        if not contact:
                contact = self.getter.get(user_ids=item,fields=self.fields)[0]
                uid = str(contact.get('id',item))
                self.cl[uid] =  contact
                if contact.get('screen_name'):
                    self.cl[contact.get('screen_name')]=contact
            # filename,headers = urllib.urlretrieve(contact.get('photo_50'))
            # contact.setdefault('photo_cache',filename)
        return contact

    def get(self,item,fallback=None):
        try:
            return self.__getitem__(item)
        except:
            return fallback

    def cleanup(self):
        for contact in self.cl.values():
            filename = contact.get("photo_cache")
            if filename:
                try:
                    os.remove(filename)
                except OSError,e:
                    logger.debug(str(e))

class VkMessenger(object):
    def __init__(self,CLIENT_ID=CLIENT_ID, CLIENT_SECRET=CLIENT_SECRET, CLIENT_SCOPE=CLIENT_SCOPE):
        self.Api = vkcom.api.API(CLIENT_ID, CLIENT_SECRET, CLIENT_SCOPE)

    #@loggit(logger)
    def login(self,username=None,password=None,token=None):
        self.Api.login(access_token=token,username=username,password=password)

    @loggit(logger)
    def connect(self):
        lp = self.Api.messages.getLongPollServer()
        server = lp.pop('server')
        host,path = server.split('/',1)
        path = '/' + path
        lp.setdefault('wait',WAIT)
        lp.setdefault('act','a_check')
        lp.setdefault('mode',MODE)
        args = (host,path,lp)
        self._connected = True
        logger.debug('start polling')
        threading.Thread(target=self.poll,args=args).start()

    def poll(self,host,path,lp):
        # uri = LP_URI.format(**self.lp)
        logger.debug('started polling')

        # try:
        while self._connected:
            conn = httplib.HTTPConnection(host)
            parameters = urllib.urlencode(lp)
            conn.request("POST", path , parameters)
            response = conn.getresponse()
            if response.status == 200:
                # text = response.read()
                # logger.debug(text)
                # data = json.loads(text)
                data = json.load(response)
                conn.close()
                logger.info(repr(data))
                if data.get('failed'):
                    break
                lp['ts']=data.get('ts',lp['ts'])
                for update in data.get("updates",[]):
                    self.update(update)
            else:
                conn.close()
                #self.disconnect()
                break
        # except Exception,e:
        #     logger.error(e.message)


        if self._connected:
            self.connect()
        else:
            self._disconnected()

    def disconnect(self):
        self._connected=False

    def _disconnected(self):
        logger.info('Polling stoped')

    def update(self,update):
        logger.debug(repr(update))
        code = update[0]
        flags = update[2]
        if code == 4 :
            message=update[3:]
            if flags & 2:
                self.outgoing_message(update[1],*message)
            else:
                self.incoming_message(update[1],*message)
        elif code == 9:
            self.friend_offline(-update[1])
        elif code == 8:
            self.friend_online(-update[1])


    def incoming_message(self,message_id,uid,timestamp,title,text,attachments=None):
        logger.debug((message_id,uid,timestamp,title,text,attachments))

    def outgoing_message(self,message_id,uid,timestamp,title,text,attachments=None):
        logger.debug((message_id,uid,timestamp,title,text,attachments))

    def send_text(self,user,message):
        try:
            user_id = int(user,10)
            domain = None
        except ValueError:
            domain = str(user)
            user_id = None
        message=message.encode('utf-8')
        resp = self.Api.messages.send(user_id=user_id,domain=domain,message=message)
        return resp

    def markAsRead(self,message_ids,user_id):
        self.Api.messages.markAsRead(message_ids=message_ids,user_id=user_id)


if __name__ == "__main__" :
    messenger = VkMessenger()
    print messenger.login()
    messenger.login(link=raw_input())
    messenger.connect()

    def close(*args):
        threading.Thread(target=messenger.disconnect).start()

    signal.signal(signal.SIGINT,close)
    while messenger._connected: time.sleep(1)