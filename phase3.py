#! /usr/bin/env python3

from bsddb3 import db
from dataclasses import dataclass

'''
alphanumeric    ::= [0-9a-zA-Z_-]
numeric		::= [0-9]
date            ::= numeric numeric numeric numeric '/' numeric numeric '/' numeric numeric
datePrefix      ::= 'date' whitespace* (':' | '>' | '<' | '>=' | '<=')
dateQuery       ::= datePrefix whitespace* date
emailterm	::= alphanumeric+ | alphanumeric+ '.' emailterm
email		::= emailterm '@' emailterm
emailPrefix	::= (from | to | cc | bcc) whitespace* ':'
emailQuery	::= emailPrefix whitespace* email
term            ::= alphanumeric+
termPrefix	::= (subj | body) whitespace* ':'
termSuffix      ::= '%' 
termQuery       ::= termPrefix? whitespace* term termSuffix?

expression      ::= dateQuery | emailQuery | termQuery 
query           ::= expression (whitespace expression)*

modeChange	::= 'output=full' | 'output=brief'

command		::= query | modeChange
'''

class Query:
    pass

@dataclass
class DateQuery(Query):
    date_prefix: str
    date: str

class ModeChange:
    pass

class Parser:

    def __init__(self, s):
        self.index = 0
        self.string = s

    def parse(self) -> Query:
        #try:
        #    return self.dateQuery()
        #except DateParseException:
        #    print("REEEEEEEEEEEEEEEEEE")
        return self.dateQuery()

    def chomp_whitespace(self) -> None:
        while self.string[self.index + 1] == " ":
            self.string = self.string[:self.index] + self.string[self.index + 1:]

    # dateQuery ::= datePrefix whitespace* date
    def dateQuery(self) -> DateQuery:
        pre: str = self.datePrefix()
        self.chomp_whitespace()
        d: str = self.date()
        return DateQuery(pre, d)

    # datePrefix ::= 'date' whitespace* (':' | '>' | '<' | '>=' | '<=')
    def datePrefix(self) -> str:

        if self.string[self.index:self.index+4] != "date":
            raise DateParseException()
        
        self.index += 4
        self.chomp_whitespace()
        tok = self.string[self.index+1]
        if tok in (':', '>', '<', '>=', '<='):
            return self.string[:self.index]
        
        raise DateParseException()
    
    def date(self) -> str:
        date_regex = re.compile(r"\d{4}\/\d{2}\/\d{2}")
        match = date_regex.match(self.string)
        if (m.start() == self.index):
            self.index = m.end()
            return self.string[m.start():m.end()]

        raise DateParseException()
 
class ParseException(Exception):
    pass
class DateParseException(ParseException):
    pass


# test
p = Parser(":     2000/11/11")

idk = p.parse()

print(idk.date_prefix)
print(idk.date)
