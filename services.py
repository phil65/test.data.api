# -*- coding: utf-8 -*-
import urllib
import json
import time
import urllib2
import gzip
import StringIO
import re
import traceback

SERVER = "http://api.rrmj.tv"


def GetHttpData(url, data=None, cookie=None, headers=None):
    try:
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) {0}{1}'.
                       format('AppleWebKit/537.36 (KHTML, like Gecko) ',
                              'Chrome/28.0.1500.71 Safari/537.36'))
        req.add_header('Accept-encoding', 'gzip')
        if cookie is not None:
            req.add_header('Cookie', cookie)
        if headers is not None:
            for header in headers:
                req.add_header(header, headers[header])
        if data:
            response = urllib2.urlopen(req, data, timeout=3)
        else:
            response = urllib2.urlopen(req, timeout=3)
        httpdata = response.read()
        if response.headers.get('content-encoding', None) == 'gzip':
            httpdata = gzip.GzipFile(fileobj=StringIO.StringIO(httpdata)).read()
        response.close()
        match = re.compile('encoding=(.+?)"').findall(httpdata)
        if not match:
            match = re.compile('meta charset="(.+?)"').findall(httpdata)
        if match:
            charset = match[0].lower()
            if (charset != 'utf-8') and (charset != 'utf8'):
                httpdata = unicode(httpdata, charset).encode('utf8')
    except Exception:
        traceback.print_exc()
        httpdata = '{"status": "Fail"}'
    return httpdata


class FakeSettings(object):

    def __init__(self):
        self.settings = {}

    def getSetting(self, name):
        return self.settings.get(name)

    def setSetting(self, name, value):
        self.settings[name] = value


__ADDON__ = FakeSettings()


FAKE_HEADERS = {
    "a": "cf2ecd4d-dea3-40ca-814f-3f0462623b1c",
    "b": "",
    "clientType": "android_%E5%B0%8F%E7%B1%B3",
    "clientVersion": "99.99",
    "c": "5a1fb134-9384-4fc8-a5ae-6e711e24afc1",
    "d": "",
    "e": "d4dd075d894dd2b8c81f96062dbe7dcbf7d467fd"
}


def getGUID():
    return "key123455"


def createKey():
    constantStr = "yyets"
    c = str(int(time.time())) + "416"
    return caesarEncryption(constantStr + c, 3)


def caesarEncryption(source, offset):
    dic = "abcdefghijklmnopqrstuvwxyz0123456789"
    length = len(dic)
    result = ""
    for ch in source:
        i = dic.find(ch)
        if i + offset >= length:
            result += dic[(i + offset) % length]
        else:
            result += dic[i + offset]
    return result


class MeiJu(object):

    """docstring for RenRenMeiJu"""

    def __init__(self):
        self._header = FAKE_HEADERS
        key_id = getGUID()
        self._header.update(a=key_id)
        self.get_ticket()

    def get_json(self, url, data=None, pretty=False):
        headers = self.header
        headers.update(b=url)
        s = json.loads(GetHttpData(url, data=data, headers=headers))
        # if pretty:
        #     xbmc.log(json.dumps(s, sort_keys=True,
        #                         indent=4, separators=(',', ': ')))
        return s

    def get_ticket(self):
        expired_time = __ADDON__.getSetting("expired_time")
        if expired_time != "":
            now = int(time.time()) * 1000
            if now < int(expired_time):
                return
        API = '/auth/ticket'
        auth_data = {"a": FAKE_HEADERS["a"],
                     "b": createKey()}
        data = self.get_json(SERVER + API, data=urllib.urlencode(auth_data))
        if data["data"]["ticket"] != "":
            __ADDON__.setSetting("expired_time", str(data["data"]["expiredTime"]))

    @property
    def header(self):
        self._header.update(d=str(int(time.time())) + "416")
        return self._header

    def search(self, page=1, rows=12, **kwargs):
        API = '/v2/video/search'
        kwargs["page"] = page
        kwargs["rows"] = rows
        return self.get_json(SERVER + API, data=urllib.urlencode(kwargs))

    def get_album(self, albumId=2):
        API = '/v2/video/album'
        return self.get_json(SERVER + API, data=urllib.urlencode(dict(albumId=albumId)))

    def index_info(self):
        API = '/v2/video/indexInfo'
        return self.get_json(SERVER + API)

    def video_detail(self, seasonId, userId=0, **kwargs):
        API = '/v2/video/detail'
        kwargs["seasonId"] = seasonId
        kwargs["userId"] = userId
        return self.get_json(SERVER + API, data=urllib.urlencode(kwargs))

    def hot_word(self):
        API = '/v2/video/hotWord'
        return self.get_json(SERVER + API)
