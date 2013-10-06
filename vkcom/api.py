# -*- coding:utf-8 -*-
__author__ = 'eri'

version = (5, 0)
str_version = '.'.join(str(v) for v in version)

import httplib
import urllib
try:
    import simplejson as json
except ImportError:
    import json

import logging
import logging.handlers

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger('Vk API')


class APIError(Exception):
    """
    1	Unknown error occurred.
    2	Application is disabled. Enable your application or use test mode.
    4	Incorrect signature.
    5	User authorization failed.
    6	Too many requests per second.
    7	Permission to perform this action is denied by user.
    """
    def __init__(self, response):
        self.response = response
        self.message = self.response['error_msg']
        self.response['error_code'] = int(self.response['error_code'])
    def __str__(self):
        return self.message
    def __getitem__(self, item):
        return self.response[item]

    def __int__(self):
        return self.response['error_code']

class AuthError(Exception):
    def __init__(self, response):
        self.response = response
        self.error = response.get('error')
        self.message = response.get('error_description',self.error)

    def __str__(self):
        return '{}: {}'.format(self.error,self.message)

    def __unicode__(self):
        return self.message



class Method(object):
    access_token = None
    v=str_version
    lang=None
    https=None
    method=[]

    def call(self, method, **kwargs):
        """
        https://api.vk.com/method/METHOD_NAME?PARAMETERS&access_token=ACCESS_TOKEN
        """
        logger.info(method)
        if not method:
            raise NameError('method is not provided')

        parameters={
            'access_token':self.access_token,
            'v':self.v
        }
        parameters.update(kwargs)

        parameters = dict((k,v) for k,v in parameters.items() if v)

        logger.debug(repr(parameters))

        lists = dict((k,','.join(map(str,v))) for k,v in parameters.items() if type(v) == list)
        parameters.update(lists)

        parameters = urllib.urlencode(parameters)
        conn = httplib.HTTPSConnection("api.vk.com")
        conn.request("POST", "/method/" + method , parameters)
        response = conn.getresponse()
        # data = response.read()
        data = json.load(response)
        conn.close()

        if 'error' in data.keys():
            raise APIError(data['error'])

        return data.get('response')

    def __call__(self, *args, **kwargs):
        return self.call('.'.join(self.method), **kwargs)

    def __getattr__(self,name):
       cp = Method()
       cp.access_token = self.access_token
       cp.v = self.v
       cp.method = self.method + [name]
       return cp


class API(Method):
    def __init__(self, client_id, client_secret=None, scope=None,v=str_version,lang=None,https=None):
        self.expires_in = None
        self.user_id = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self.v = v
        self.lang=lang
        self.https = https

    def _direct_auth(self,username=None,password=None,**kwargs):
        parameters = {
            'grant_type':'password',
            'client_id':self.client_id,
            'client_secret':self.client_secret,
            'username':username,
            'password':password,
            'v':self.v
        }

        if self.scope: parameters.update({'scope':self.scope})
        parameters.update(kwargs)

        parameters = urllib.urlencode(parameters)
        conn = httplib.HTTPSConnection("oauth.vk.com")
        conn.request("GET", "/token?" + parameters)
        response = conn.getresponse()
        data = json.load(response)
        conn.close()
        if 'error' in data.keys():
            raise AuthError(data)

        self.access_token = data.get('access_token')
        self.user_id = data.get('user_id')
        self.expires_in = data.get('expires_in')

        return True
    def _link(self,link):
        '''https://oauth.vk.com/blank.html
        #access_token=964ef3f76bd4f36ac9a58a928d0ceaccf3524301aefb082b703f25a5f78f7714a96d7ec4ca4ca6c336371&
        expires_in=0&
        user_id=136195746'''

        self.access_token = link.split("access_token=")[-1].split("&")[0]
        self.user_id = link.split("user_id=")[-1].split("&")[0]
        self.expires_in = link.split("expires_in=")[-1].split("&")[0]

    def auth_link(self,display='mobile',redirect_uri='https://oauth.vk.com/blank.html',response_type='token', **kwargs):
        '''https://oauth.vk.com/authorize?
        client_id=APP_ID&
        scope=PERMISSIONS&
        redirect_uri=REDIRECT_URI&
        display=DISPLAY&
        v=API_VERSION&
        response_type=token'''

        parameters = {
            'client_id':     self.client_id,
            'display':       display,
            'redirect_uri':  redirect_uri,
            'response_type': response_type,
            'v':             self.v,
            'scope':         self.scope
        }
        parameters.update(kwargs)
        parameters = urllib.urlencode(parameters)
        return 'https://oauth.vk.com/authorize?' + parameters

    def _mechanize(self,username, password, **kwargs):

        import mechanize
        parameters = {
            'client_id': self.client_id,
            'scope': self.scope,
            'redirect_uri': "http://oauth.vk.com/blank.html",
            'display': 'wap',
            'response_type': "token"
        }

        parameters = urllib.urlencode(parameters)
        login_uri = 'https://api.vk.com/oauth/authorize?' + parameters
        br = mechanize.Browser()
        br.set_handle_equiv(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        br.open(login_uri)
        br.select_form(predicate=lambda f: 'method' in f.attrs and f.attrs['method'] == "post")
        br['email']=username
        br['pass']=password
        resp = br.submit()
        uri = resp.geturl()
        if uri.find('access_token') > 1:
            return self._link(uri)
        else :
            #'запрос разрешений'
            br.select_form(predicate=lambda f: 'method' in f.attrs and f.attrs['method'] == "post")
            resp = br.submit()
            uri = resp.geturl()
            if uri.find('access_token') > 1:
                return self._link(uri)
            else:
                raise AuthError({'error':'unexpected url','error_description':uri})


        pass

    def login(self, link=None, access_token=None, user_id=None, expires_in=None, username=None, password=None, **kwargs):

        if username and password:
            try:
                logger.info('Direct Auth')
                self._direct_auth(username=username, password=password, **kwargs)
            except:
                logger.info('Mechnize Auth')
                self._mechanize(username=username, password=password, **kwargs)

        if access_token:
            logger.info('Have Token')
            self.access_token = access_token
            self.user_id = user_id
            self.expires_in = expires_in
            return True

        if link:
            logger.info('Parsing Link')
            self._link(link)

        return self.auth_link(**kwargs)


