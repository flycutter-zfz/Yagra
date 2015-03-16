#!/usr/bin/env python
# encoding: utf-8

import cgi, os, hashlib

form = cgi.FieldStorage()
username = form['username'].value
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

print """Content-type: text/html\n
<html>
<body>
<p>%s</p>
</body>
</html>""" % message
