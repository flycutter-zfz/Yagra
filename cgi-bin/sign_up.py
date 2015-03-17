#!/usr/bin/env python
# encoding: utf-8

import cgi
import Mysql
import os
import binascii
import hashlib
import Cookie

form = cgi.FieldStorage()
username = form['username'].value
password = form['password'].value

#Connect to MySQL
mysql = Mysql.Mysql()
cursor = mysql.cursor

#Check whether the username is already exists.
sql = 'select * from user where username = %s'
param = username
n = cursor.execute(sql, param)
if n > 0:
    message = "The username has been registered, please choose another one."
else:
    salt = binascii.b2a_hex(os.urandom(32))
    hashed_password = hashlib.sha256(salt+password).hexdigest()
    sql = 'insert into user(username, password, salt) values (%s, %s, %s)'
    param = (username, hashed_password, salt)
    n = cursor.execute(sql, param)
    message = "Sign up successfully!"

mysql.close()

print 'Content-type: text/html\n'
template_html = open(r'../www/template.html').read()
print template_html % message
