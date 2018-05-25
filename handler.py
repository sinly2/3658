# -*- coding: utf-8 -*-
"""
Created on Jan 24, 2018

@author: guxiwen
"""
from base import Session
import threading, time
import redis


class Handler(threading.Thread):
    def __init__(self, threadName, username, password, trade_password):
        super(Handler, self).__init__(name=threadName)
        self.session = Session(username, password, trade_password)

    def run(self):
        count = 1
        while not self.session.login() and count < 10:
            time.sleep(5)
            count = count + 1
        if self.session.flag is False:
            print 'login failed...'
        while self.session.flag:
            if self.session.withdraw(960, 117166):
                break
            time.sleep(5)


class LoginHandler(threading.Thread):
    def __init__(self, threadName, username, password, trade_password):
        super(LoginHandler, self).__init__(name=threadName)
        self.username = username
        self.session = Session(username, password, trade_password)
        self.r_connector = redis.Redis(host="127.0.0.1", port=6379, db=0)

    def run(self):
        while True:
            keys = self.r_connector.keys(self.username + "*")
            if len(keys) > 5:
                print 'sleeping'
                time.sleep(60)
            else:
                print 'logining...'
                if self.session.login():
                    self.session.store_cookie()
            time.sleep(30)


class WithdrawHandler(threading.Thread):
    def __init__(self, threadName, username, password, trade_password):
        super(WithdrawHandler, self).__init__(name=threadName)
        self.session = Session(username, password, trade_password)
        if not self.session.set_cookies():
            print 'Cookie set failed...'

    def run(self):
        while True:
            code = self.session.withdraw(200, 117166)
            if code == "1000":
                break
            elif code == "1001":
                break
            elif code == "1010":
                self.session.set_cookies()
                time.sleep(10)
            elif code == "1004":
                print '1004'
                continue
            elif code == "1005":
                break
            elif code == "1006":
                break
            elif code == "1008":
                break
            elif code == "1009":
                break
            else:
                break


class GetWithdrawDayHandler(threading.Thread):
    def __init__(self, threadName, username, password, trade_password="123456"):
        super(GetWithdrawDayHandler, self).__init__(name=threadName)
        self.session = Session(username, password, trade_password)
        if not self.session.set_cookies():
            print 'Cookie set failed...'

    def run(self):
        count = 0
        while count < 10:
            code = self.session.get_withdraw_day()
            if code == "1000":
                break
            else:
                time.sleep(1)
                count = count + 1
                continue

if __name__ == "__main__":
    pass
