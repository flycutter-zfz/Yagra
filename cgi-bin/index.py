#!/usr/bin/env python
# encoding: utf-8

import Cookie
import os
import MySQLdb
import time
import hashlib

cookie = Cookie.SimpleCookie()
string_cookie = os.environ.get('HTTP_COOKIE')

is_login = False

#check content of cookie
if string_cookie:
    cookie.load(string_cookie)
    if cookie.has_key('username') and cookie.has_key('sid'):
        username = cookie['username'].value
        sid = cookie['sid'].value
        conn = MySQLdb.connect(host='localhost',user='yagra',passwd='yagratest',
                db='Yagra', charset='utf8')
        cursor = conn.cursor()
        sql = 'select sid, expires, lastvisit from session where username=%s'
        param = (username)
        n = cursor.execute(sql, param)
        #if has session, sid match, and the time is not expire.
        if n > 0:
            row = cursor.fetchone()
            if row[0] == sid and int(time.time()) - row[2] < row[1]:
                is_login = True
                sql = 'update session set lastvisit = %s where username=%s'
                param = (int(time.time()), username)
                cursor.execute(sql, param)
        conn.commit()
        cursor.close()
        conn.close()

print 'Content-type: text/html\n'

if is_login:
    #The profile page.
    hashcode = hashlib.md5(username.strip().lower()).hexdigest()
    profile_html = open(r'../www/profile.html').read()
    print profile_html % (hashcode, hashcode)
else:
    #The login page.
    login_html = open(r'../www/login.html').read()
    print login_html
