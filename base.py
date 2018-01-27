# -*- coding: utf-8 -*-
"""
Created on Jan 23, 2018

@author: guxiwen
"""
import requests
import redis


class Session(object):

    def __init__(self, username, password, trade_password):
        self.session = requests.Session()
        self.r_connector = redis.Redis(host="127.0.0.1", port=6379, db=0)
        self.username = username
        self.password = password
        self.trade_password = trade_password
        self.timeout = 60
        self.flag = False
        self.keys = []
        self.key = ""
        self.withdraw_url = "https://www.3658mall.com/user.php"
        self.user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 " \
                          "Safari/537.36 SE 2.X MetaSr 1.0"
        self.headers = {"user-agent": self.user_agent, "accept-encoding": "gzip,deflate",
                        "accept-language": "zh-CN,zh;q=0.8",
                        "origin": "https://www.3658mall.com", "content-type": "application/x-www-form-urlencoded",
                        "referer":
                            "https://www.3658mall.com/member.html", "Connection": "keep-alive"}

    def close_session(self):
        self.session.close()

    def store_cookie(self):
        cookies = requests.utils.dict_from_cookiejar(self.session.cookies)
        self.r_connector.set(self.username + ":" + str(hash(str(cookies))), cookies, 1800)

    def set_cookies(self):
        self.keys = self.r_connector.keys(self.username + "*")
        if self.keys:
            self.key = self.keys.pop()
            cookies = self.r_connector.get(self.key)
            cookies = eval(cookies)
            cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
            self.session.cookies = cookies
            return True
        else:
            return False

    def clear_cookies(self):
        cookies = requests.utils.cookiejar_from_dict({}, cookiejar=None, overwrite=True)
        self.session.cookies = cookies

    def cookie_is_available(self):
        pass

    def login(self,act="act_login_new"):
        self.clear_cookies()
        params = {"username": self.username, "password": self.password, "msgCode": "","act":act}
        try:
            result = self.session.post(self.withdraw_url, data=params, headers=self.headers, timeout=self.timeout)
            # print result.text
            # print result.headers
            # print result.status_code
            if result.status_code == 200 and result.json()["status"] is True:
                self.flag = True
                return True
            else:
                return False
        except Exception, e:
            return False
            print e

    def withdraw(self, amount, bank_id, surplus=1, act="act_account"):
        """
        :return:
        1000 提现成功
        1001 额度用完
        1010 重新登陆
        1003 http返回200，未知错误
        1004 http返回非200
        1005 七日提现限制
        1006 个人周提现限制
        1007 提现金额不是20的整数倍
        1008 支付密码错误
        """
        params = {"amount": amount, "raply_bank": bank_id, "surplus_type": surplus, "act": act,
                  "p_password": self.trade_password, "raply_type": 0}
        try:
            result = self.session.post(self.withdraw_url, data=params, headers=self.headers, timeout=self.timeout)
            # print result.status_code
            # print result.headers
            if result.text.find(u"当日系统限额已用完，请明天提交提现申请！") != -1:
                self.flag = False
                print u'当日额度已用完！'
                return "1001"
            if result.status_code == 200:
                if u"提交成功，银行处理中" in result.text:
                    print '%s 提交成功，银行处理中...' % (self.username)
                    return "1000"
                elif u"立即注册" in result.text and u"使用合作网站账号登录" in result.text:
                    print '%s session丢失，请重新登陆...' % (self.username)
                    return "1010"
                elif u"7天内仅允许1次提现，请您耐心等待！" in result.text:
                    print '%s 7天内仅允许1次提现，请您耐心等待！' % (self.username)
                    return "1005"
                elif u"提现红金宝超出每周提现的限额" in result.text:
                    print "%s 提现超出每周提现的限额" % (self.username)
                    return "1006"
                elif u"提现失败，提现金额必须是20的整数倍" in result.text:
                    print '%s 提现失败，提现金额必须是20的整数倍...' % (self.username)
                    return "1007"
                elif u"支付密码错误，请重新输入" in result.text:
                    print '%s 支付密码错误，请重新输入' % (self.username)
                    return "1008"
                else:
                    print result.text
                    print '%s unkown mistakes...' % (self.username)
                    return "1003"
            else:
                print '%s withdraw httpresponse code %s' % (self.username, str(result.status_code))
                return "1004"
        except Exception, e:
            print e
            return "1003"

    def withdraw_hjb(self, amount, bank_id):
        """

        :return:
        1000 提现成功
        1001 提现失败，服务端限制
        1002 提现失败，抛出异常
        1010 提现失败，需要登陆
        """
        try:
            params = {"amount": amount, "raply_bank": bank_id, "act": "act_integ", "p_password": self.trade_password}
            result = self.session.post(self.withdraw_url, data=params, headers=self.headers, timeout=self.timeout)
            if u"立即注册" in result.text and u"使用合作网站账号登录" in result.text:
                print "%s 提现红金宝需要登陆..." % (self.username)
                return "1010"
            if result.json()["status"] == "error":
                print "%s %s " % (self.username,result.json()["message"])
                return "1001"
            return "1000"
        except Exception, e:
            print e
            return "1002"

    def change_password(self, uid, new_password):
        params = {"uid": uid, "new_password": new_password, "is_mobile": 1}
        url = "https://www.3658mall.com/user.php?act=act_edit_password_mobile"
        result = self.session.post(url, data=params, headers=self.headers, timeout=self.timeout)
        print result.text
        print result.json()["msg1"]

    def day_sign(self):
        """

        :return:
        1000 签到成功
        1001 需要登陆
        1002 今日已签到
        1003 未知错误
        """
        params = {}
        url = "https://www.3658mall.com/day_sign.php?act=just_sign"
        result = self.session.post(url, data=params, headers=self.headers, timeout=self.timeout)
        if u"立即注册" in result.text and u"使用合作网站账号登录" in result.text:
            print "%s session丢失，请重新登陆..." % (self.username)
            return "1001"
        elif result.json()["error"] == 1 and result.json()["content"] == u"今日已签到，明日再来吧！":
            print u"%s 今日已签到！" % (self.username)
            return "1002"
        elif result.json()["error"] == 1:
            print '%s unkown mistakes...' % (self.username)
            print result.json()["content"]
            return "1003"
        url = "https://www.3658mall.com/day_sign.php"
        result = self.session.get(url, headers=self.headers, timeout=self.timeout)
        url = "https://www.3658mall.com/day_sign.php?act=sign"
        result = self.session.post(url, data=params, headers=self.headers, timeout=self.timeout)
        if result.json()["code"] == 99:
            print "%s 签到成功!" % (self.username)
            return "1000"
        else:
            print '%s unkown mistakes...' % (self.username)
            print result.json()["content"]
            return "1003"


if __name__ == "__main__":
    pass
