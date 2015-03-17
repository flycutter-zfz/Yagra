#!/usr/bin/env python
# encoding: utf-8

import MySQLdb

class Mysql(object):

    def __init__(self):
        self.conn = MySQLdb.connect(host='localhost', user='yagra', passwd='yagratest',
                db='Yagra', charset='utf8')
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

