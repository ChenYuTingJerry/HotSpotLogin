from httplib2 import Http, ServerNotFoundError
from urllib import urlencode
from scrapy.http import HtmlResponse
from scrapy.selector import Selector
from lxml import html
import socket


class Logger(object):
    CHECK_URL = 'https://facebook.com'
    TYPE_URL_ENCODED = 'application/x-www-form-urlencoded'
    KEY_CONTENT_TYPE = 'Content-Type'
    KEY_ACCEPTED_URL = 'acceptedurl'
    KEY_USER_NAME = 'username'
    KEY_PASSWORD = 'password'
    KEY_DST_URL = 'dsturl'
    KEY_DST = 'dst'
    KEY = 'key'
    TPE_USERNAME = '0920503761'
    TPE_PASSWORD = 'fuhu123'
    h = Http(timeout=10)

    def __init__(self):
        pass

    def login(self):
        print 'login'

    def logout(self):
        print 'logout'

    def has_internet_ability(self):
        try:
            resp, content = self.h.request(self.CHECK_URL)
            if resp.status == 200:
                return True
            else:
                return False
        except ServerNotFoundError:
            print 'server not found'
            return False
        except socket.error:
            print 'socket error'
            return False


class TpeLogger(Logger):
    """
    Auto-Login TPE-Free hotspot
    """
    URL_REFER = 'https://member.wifly.com.tw/WiflyConn/LoginS1.aspx'
    URL_ACCEPTED = "http://www.tpe-free.taipei.gov.tw/TPE/taipei_index.html"
    # URL_LOGIN = "https://apc.aptilo.com/cgi-bin/login"
    URL_LOGIN = 'https://wac.wifly.com.tw/login'
    URL_LOGOUT = "http://ap.logout/"
    TAG_NAME = 'tpe-free.tw/'

    def __init__(self):
        super(TpeLogger, self).__init__()

    def login(self):
        headers = {self.KEY_CONTENT_TYPE: self.TYPE_URL_ENCODED}
        post_data = {self.KEY_USER_NAME: self.TAG_NAME + self.TPE_USERNAME,
                     self.KEY_PASSWORD: self.TPE_PASSWORD}

        try:
            resp, content = self.h.request(uri=self.URL_LOGIN,
                                           method='POST',
                                           headers=headers,
                                           body=urlencode(post_data))
            if resp.status == 200:
                resp, content = self.h.request(self.URL_ACCEPTED)
                if resp.status == 200:
                    return True
                elif resp.status == 302 and self.has_internet_ability():
                    return True
                else:
                    return False
            else:
                return False
        except socket.error as m:
            print m.message
            return False
        except ServerNotFoundError as m:
            return False

    def logout(self):
        try:
            resp, content = self.h.request(self.URL_LOGOUT)
            if resp.status == 200:
                return True
            else:
                return False
        except socket.error as m:
            return False
        except ServerNotFoundError as m:
            return False



# class WiFlyLogger(Logger):
#     """
#     Auto-Login WiFly hotspot
#     """
#     URL_FIRST = 'http://www.wifly.com.tw/superwifi/4FreeLogin.aspx'
#     URL_SECOND = 'https://www.wifly.com.tw/superwifi/4FreeLogin.aspx'
#     URL_JUMP_PAGE = 'http://www.4free.com.tw/wifly/login'
#     URL_LOGIN = 'https://wac.wifly.com.tw/login'
#     URL_DEST = 'http://www.4free.com.tw/'
#
#     def __init__(self):
#         super(WiFlyLogger, self).__init__()
#
#     def login(self):
#         # TODO reduce the login steps
#         try:
#             resp, content = self.h.request(self.URL_FIRST)
#             userInfo = dict()
#             if resp.status == 200:
#                 tree = html.fromstring(content)
#                 for element in tree.xpath('//input[@type="hidden"]'):
#                     userInfo[element.attrib['name']] = element.attrib['value']
#                 userInfo[self.KEY_DST_URL] = self.URL_DEST
#                 print userInfo
#                 post_data = {'mac': userInfo['mac'],
#                              'loginkey': userInfo['loginkey'],
#                              self.KEY_DST_URL: userInfo[self.KEY_DST_URL]}
#                 headers = {self.KEY_CONTENT_TYPE: self.TYPE_URL_ENCODED}
#                 print post_data
#                 print headers
#                 resp, content = self.h.request(self.URL_SECOND,
#                                                method='POST',
#                                                body=urlencode(post_data),
#                                                headers=headers)
#                 if resp.status == 200:
#                     userInfo.clear()
#                     tree = html.fromstring(content)
#                     for element in tree.xpath('//input[@type="hidden"]'):
#                         userInfo[element.attrib['name']] = element.attrib['value']
#
#                     post_data = {self.KEY_USER_NAME: userInfo[self.KEY_USER_NAME],
#                                  self.KEY_PASSWORD: userInfo[self.KEY_PASSWORD]}
#                     resp, content = self.h.request(self.URL_LOGIN,
#                                                    method='POST',
#                                                    body=urlencode(post_data),
#                                                    headers=headers)
#                     print content
#                     return True
#         except socket.error as m:
#             return False
#         except ServerNotFoundError as m:
#             return False

# class WiFlyLogger(Logger):
#     """
#     Auto-Login WiFly hotspot
#     """
#     URL_ENTRY = 'https://www.wifly.com.tw/superwifi/4FreeLogin.aspx'
#     URL_JUMP_PAGE = 'http://www.4free.com.tw/wifly/login'
#     URL_LOGIN = 'https://wac.wifly.com.tw/login'
#     URL_DEST = 'http://www.4free.com.tw/'
#
#     def __init__(self):
#         super(WiFlyLogger, self).__init__()
#
#     def login(self):
#         # TODO reduce the login steps
#         try:
#             resp, content = self.h.request(self.URL_ENTRY)
#             userInfo = dict()
#             if resp.status == 200:
#                 # print content
#                 for item in Selector(text=content).xpath('//input[@type="hidden"]'):
#                     userInfo[item.xpath('@name').extract()[0]] = item.xpath('@value').extract()[0]
#                 print userInfo
#                 post_data = {'mac': userInfo['mac'],
#                              'loginkey': userInfo['loginkey']}
#                 headers = {self.KEY_CONTENT_TYPE: self.TYPE_URL_ENCODED}
#                 resp, content = self.h.request(self.URL_JUMP_PAGE,
#                                                method='POST',
#                                                body=urlencode(post_data),
#                                                headers=headers)
#                 print content
#                 if resp.status == 200 or resp.status == 302:
#                     userInfo.clear()
#                     for item in Selector(text=content).xpath('//input[@type="hidden"]'):
#                         userInfo[item.xpath('@name').extract()[0]] = item.xpath('@value').extract()[0]
#
#                     post_data = {self.KEY_USER_NAME: userInfo[self.KEY_USER_NAME],
#                                  self.KEY_PASSWORD: userInfo[self.KEY_PASSWORD]}
#                     resp, content = self.h.request(self.URL_LOGIN,
#                                                    method='POST',
#                                                    body=urlencode(post_data),
#                                                    headers=headers)
#                     return True
#
#         except socket.error as m:
#             return False
#         except ServerNotFoundError as m:
#             return False

class WiFlyLogger(Logger):
    """
    Auto-Login WiFly hotspot
    """
    URL_ENTRY = 'https://www.wifly.com.tw/superwifi/4FreeLogin.aspx'
    URL_JUMP_PAGE = 'http://pc.4free.com.tw/wifly/login'
    URL_JUMP_PAGE_2 = 'http://pc.4free.com.tw/wifly/login_content'
    # URL_LOGIN = 'https://wac.wifly.com.tw/login_content'

    def __init__(self):
        super(WiFlyLogger, self).__init__()

    def login(self):
        # TODO reduce the login steps
        try:
            resp, content = self.h.request(self.URL_ENTRY)
            userInfo = dict()
            if resp.status == 200:
                for item in Selector(text=content).xpath('//input[@type="hidden"]'):
                    name = item.xpath('@name').extract()[0]
                    if not name.startswith('__'):
                        userInfo[item.xpath('@name').extract()[0]] = item.xpath('@value').extract()[0]
                post_data = userInfo
                resp, content = self.h.request(self.URL_JUMP_PAGE_2+'?'+urlencode(post_data))

                for item in Selector(text=content).xpath('//div[@data-source="aplogin"]'):
                    print item.xpath('').extract()

        except socket.error as m:
            return False
        except ServerNotFoundError as m:
            return False


class ITaiwanLogger(Logger):
    """
    Auto-Login iTaiwan hotspot
    """
    URL_LOGIN = 'https://wlanac.hinet.net/loginpages/userlogin.shtml'
    URL_LOGOUT = "http://88.gov/"
    PRE_TAG_NAME = 'tpe_itw/'
    POST_TAG_NAME = '@itw'

    def __init__(self):
        pass

    def login(self):
        try:
            headers = {self.KEY_CONTENT_TYPE: self.TYPE_URL_ENCODED}
            post_data = {self.KEY_USER_NAME: self.PRE_TAG_NAME+self.TPE_USERNAME+'.tpe' + self.POST_TAG_NAME,
                         self.KEY_PASSWORD: self.TPE_PASSWORD}

            resp, content = self.h.request(self.URL_LOGIN,
                                           method='POST',
                                           body=urlencode(post_data),
                                           headers=headers)
            print resp.status
            if resp.status == 200:
                return True
            elif resp.status == 302 and self.has_internet_ability():
                return True
            else:
                return False
        except socket.error as m:
            return False
        except ServerNotFoundError as m:
            return False

    def logout(self):
        try:
            resp, content = self.h.request(self.URL_LOGOUT)
            if resp.status == 200:
                return True
            else:
                return False
        except socket.error as m:
            return False
        except ServerNotFoundError as m:
            return False


class FamiLogger(Logger):
    """
    Auto-Login FamiWifi hotspot (only 3 times a day)
    """
    URL_TRY = 'http://apc.aptilo.com/cgi-bin/auto'
    URL_LOGIN = 'https://www.wifihub.org/familymart-wifi/login_submit.php'

    def __init__(self):
        pass

    def login(self):
        try:
            userInfo = dict()
            resp, content = self.h.request(self.URL_TRY, method='GET')

            for item in Selector(text=content).xpath('//input[@type="hidden"]'):
                userInfo[item.xpath('@name').extract()[0]] = item.xpath('@value').extract()[0]

            headers = {self.KEY_CONTENT_TYPE: self.TYPE_URL_ENCODED}
            post_data = {self.KEY: userInfo[self.KEY],
                         'msisdn': '0920503761',
                         self.KEY_PASSWORD: 'fuhufuhu123'}
            resp, content = self.h.request(self.URL_LOGIN,
                                           method='POST',
                                           body=urlencode(post_data),
                                           headers=headers)
            if resp.status == 200:
                return True
            else:
                return False

        except socket.error as m:
            return False
        except ServerNotFoundError as m:
            return False


class TpeChtLogger(Logger):
    """
    Auto-Login TPE-Free_CHT hotspot
    """
    URL_ACCEPTED = "http://www.tpe-free.taipei.gov.tw/TPE/taipei_index.html"
    # URL_LOGIN = "https://apc.aptilo.com/cgi-bin/login"
    URL_LOGIN = 'https://wac.wifly.com.tw/login'
    URL_LOGOUT = "http://ap.logout/"
    TAG_NAME = 'tpe-free.tw/'

    def __init__(self):
        super(TpeChtLogger, self).__init__()

    def login(self):
        headers = {self.KEY_CONTENT_TYPE: self.TYPE_URL_ENCODED}
        post_data = {self.KEY_USER_NAME: self.TAG_NAME + self.TPE_USERNAME,
                     self.KEY_PASSWORD: self.TPE_PASSWORD}

        try:
            resp, content = self.h.request(uri="http://www.tpe-free.taipei.gov.tw/TPE/taipei_index.html",
                                           method='GET')
            print content
        except socket.error as m:
            print m.message
            return False
        except ServerNotFoundError as m:
            return False

    def logout(self):
        try:
            resp, content = self.h.request(self.URL_LOGOUT)
            if resp.status == 200:
                return True
            else:
                return False
        except socket.error as m:
            return False
        except ServerNotFoundError as m:
            return False