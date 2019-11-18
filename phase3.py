#! /usr/bin/env python3

from bsddb3 import db

DB = db.DB()

DB.open('terms.txt', None, db.DB_BTREE, db.DB_CREATE)
DB.open('emails.txt', None, db.DB_BTREE, db.DB_CREATE)
DB.open('dates.txt', None, db.DB_BTREE, db.DB_CREATE)
DB.open('recs.txt', None, db.DB_BTREE, db.DB_CREATE)

CUR = DB.cursor()

it = cur.first
while it:
    print(it)



CUR.close()
DB.close()
