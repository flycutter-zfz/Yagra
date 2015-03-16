#!/usr/bin/env python
# encoding: utf-8

import cgi
import os
import hashlib
import Cookie

cookie = Cookie.SimpleCookie()
string_cookie = os.environ.get('HTTP_COOKIE')
cookie.load(string_cookie)
username = cookie['username'].value

form = cgi.FieldStorage()
avatar = form['avatar']

def fbuffer(f, chunk_size=10000):
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        yield chunk

if avatar.filename:
    hashcode = hashlib.md5(username.strip().lower()).hexdigest()
    filepath = os.environ['DOCUMENT_ROOT'] + '/avatar/' + hashcode
    f = open(filepath, 'wb', 10000);

    for chunk in fbuffer(avatar.file):
        f.write(chunk)

    f.close()
    message = "Upload avatar successfully!"
else:
    message = "Upload avatar failed!"

print 'Content-type: text/html\n'
template_html = open(r'../www/template.html').read()
print template_html % message
