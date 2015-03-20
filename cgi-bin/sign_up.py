#!/usr/bin/env python
# encoding: utf-8

import cgi
import Mysql
import os
import binascii
import hashlib
import Cookie
import re

form = cgi.FieldStorage()
username = form['username'].value
password = form['password'].value
#Check the format of username and password
is_format_correct = len(username)>=3 and len(username)<=32 \
                    and len(password)>=6 and len(username)<=32 \
                    and re.match('[0-9a-zA-Z]+$',username) \
                    and re.match('[0-9a-zA-Z]+$',password)


if is_format_correct:
    #Connect to MySQL
    mysql = Mysql.Mysql()
    cursor = mysql.cursor

    #Check whether the username is already exists.
    sql = 'select * from user where username = %s'
    param = username
    n = cursor.execute(sql, param)
    if n > 0:
        message = '''<p>The username has been registered.</p>
        <p>Please click <a href="../www/sign_up.html">Sign up</a> to sign up again.<p>'''
    else:
        salt = binascii.b2a_hex(os.urandom(32))
        hashed_password = hashlib.sha256(salt+password).hexdigest()
        sql = 'insert into user(username, password, salt) values (%s, %s, %s)'
        param = (username, hashed_password, salt)
        n = cursor.execute(sql, param)
        message = "Sign up successfully!"
    mysql.close()
else:
    message = '''<p>Invalid username or password format.</p>
        <p>Please click <a href="../www/sign_up.html">Sign up</a> to sign up again.<p>'''

print 'Content-type: text/html\n'
template_html = open(r'../www/template.html').read()
print template_html % message
