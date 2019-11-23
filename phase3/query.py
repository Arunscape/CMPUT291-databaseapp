from bsddb3 import db

from parser import parse
from constants import CONSTANTS

class Query:
    
    def __init__(self):
        self.date_db = self.get_db(CONSTANTS['DATE_INDEX'])
        self.email_db = self.get_db(CONSTANTS['EMAIL_INDEX'])
        self.term_db = self.get_db(CONSTANTS['TERM_INDEX'])


    def get_db(self, index_file):
        database = db.DB()
        database.open(index_file, None, db.DB_BTREE)
        return database

