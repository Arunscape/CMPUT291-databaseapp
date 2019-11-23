from bsddb3 import db

from parser import parse
from constants import CONSTANTS


class Query:
    def __init__(self):
        self.date_db = self.get_db(CONSTANTS["DATE_INDEX"], db.DB_BTREE)
        self.email_db = self.get_db(CONSTANTS["EMAIL_INDEX"], db.DB_BTREE)
        self.term_db = self.get_db(CONSTANTS["TERM_INDEX"], db.DB_BTREE)
        self.rec_db = self.get_db(CONSTANTS["REC_INDEX"], db.DB_HASH)

    def get_db(self, index_file, db_type):
        database = db.DB()
        database.open(index_file, None, db_type)
        return database

    def close_db(self):
        for d in (self.date_db, self.email_db, self.term_db, self.rec_db):
            d.close()

    def process(self, query):
        if query.type == "date":
            pass
        elif query.type == "email":
            pass
        elif query.type == "term":
            pass
        else:
            raise Exception("I don't know what to do")
