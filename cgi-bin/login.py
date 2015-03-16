#!/usr/bin/env python
# encoding: utf-8

import cgi
import MySQLdb
import os
import binascii
import hashlib
import Cookie
import time

form = cgi.FieldStorage()
username = form['username'].value
password = form['password'].value

#Connect to MySQL
conn = MySQLdb.connect(host='localhost',user='yagra',passwd='yagratest',
        db='Yagra',charset='utf8')
cursor = conn.cursor()

#Get the hashed password and salt from Mysql.
sql = 'select password, salt from user where username = %s'
param = username
n = cursor.execute(sql, param)

is_login_succ = False
if n > 0:
    row = cursor.fetchone()
    hashed_password = row[0]
    salt = row[1]
    tmp_password = hashlib.sha256(salt+password).hexdigest()
    if tmp_password == hashed_password:
        is_login_succ = True

if is_login_succ:
    #Set the cookie information
    cookie = Cookie.SimpleCookie()
    cookie['username'] = username
    sid = hashlib.sha256(repr(time.time())).hexdigest()
    cookie['sid'] = sid
    print cookie

    #store the session information
    sql = 'delete from session where username=%s'
    param = (username)
    cursor.execute(sql, param)

    sql = 'insert into session(username, sid, expires, lastvisit) \
            values(%s, %s, %s, %s)'
    param = (username, sid, 3*60*60, int(time.time()))
    cursor.execute(sql, param)

    #print the page.
    print 'Content-type: text/html\n'
    profile_html = open(r'../www/profile.html').read()
    print profile_html
else:
    print 'Content-type: text/html\n'
    template_html = open(r'../www/template.html').read()
    message = "Invalid username or password!"
    print template_html % message

conn.commit()
cursor.close()
conn.close()
