#!/usr/bin/env python
# encoding: utf-8

import MySQLdb
import os
import Cookie

cookie = Cookie.SimpleCookie()
string_cookie = os.environ.get('HTTP_COOKIE')
cookie.load(string_cookie)
username = cookie['username'].value

#Connect to MySQL
conn = MySQLdb.connect(host='localhost',user='yagra',passwd='yagratest',
        db='Yagra',charset='utf8')
cursor = conn.cursor()

#Delete the session information.
sql = 'delete from session where username = %s'
param = username
n = cursor.execute(sql, param)

conn.commit()
cursor.close()
conn.close()

print 'Content-type: text/html\n'
login_html = open(r'../www/login.html').read()
print login_html
