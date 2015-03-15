#!/usr/bin/env python
# encoding: utf-8

import cgi, MySQLdb, os, binascii, hashlib

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
if n > 0:
    row = cursor.fetchone()
    hashed_password = row[0]
    salt = row[1]
    tmp_password = hashlib.sha256(salt+password).hexdigest()
    if tmp_password == hashed_password:
        message = "Log in successfully!"
    else:
        message = "Invalid username or password!"
else:
    message = "Invalid username or password!"


cursor.close()
conn.close()

print """Content-type: text/html\n
<html>
<body>
<p>%s</p>
</body>
</html>""" % message
