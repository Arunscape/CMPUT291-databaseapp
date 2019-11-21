#! /usr/bin/env python3

from bsddb3 import db
from dataclasses import dataclass

import re

"""
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
"""


class Query:
    pass


@dataclass
class DateQuery(Query):
    date_prefix: str
    date: str


@dataclass
class EmailQuery(Query):
    email_prefix: str
    email_address: str


class ModeChange:
    pass


class Parser:
    def __init__(self, s):
        self.index = 0
        self.string = s

    def parse(self) -> Query:
        try:
            return self.dateQuery()
        except DateParseException as e:
            print(e)

        try:
            return self.emailQuery()
        except EmailParseException:
            pass

    def chomp(self) -> str:
        self.index += 1
        return self.string[self.index - 1]

    def chomp_whitespace(self) -> None:
        while self.string[self.index] == " ":
            self.index += 1

    ############################################################################
    # dateQuery logic
    # dateQuery ::= datePrefix whitespace* date
    def dateQuery(self) -> DateQuery:
        pre: str = self.datePrefix()
        self.chomp_whitespace()
        d: str = self.date()
        return DateQuery(pre, d)

    # datePrefix ::= 'date' whitespace* (':' | '>' | '<' | '>=' | '<=')
    def datePrefix(self) -> str:

        # chomp 'date'
        if self.string[self.index : self.index + 4] != "date":
            raise DateParseException("Could not parse datePrefix")
        self.index += 4

        self.chomp_whitespace()
        tok: str = self.chomp()

        if tok in (":", ">", "<", ">=", "<="):
            return self.string[: self.index]

        raise DateParseException("Could not parse datePrefix pt. 2")

    def date(self) -> str:

        self.chomp_whitespace()

        date_regex = re.compile(r"\d{4}\/\d{2}\/\d{2}")
        match = date_regex.search(self.string)
        if match is not None and match.start() == self.index:
            self.index = match.end()
            # if there are extra characters
            if not self.index == len(self.string):
                raise DateParseException("Error: extra characters after date")

            return self.string[match.start() : match.end()]

        raise DateParseException("Could not parse date")

    ############################################################################

    # emailQuery
    # emailterm	::= alphanumeric+ | alphanumeric+ '.' emailterm
    # email		::= emailterm '@' emailterm
    # emailQuery	::= emailPrefix whitespace* email
    ############################################################################
    def emailQuery(self) -> EmailQuery:
        pre: str = self.emailPrefix()
        self.chomp_whitespace()
        email = self.email_address()

        return EmailQuery(pre, email)

    # emailPrefix ::= (from | to | cc | bcc) whitespace* ':'
    def emailPrefix(self) -> str:
        prefix: str
        if self.string[:2] in ("cc", "to"):
            self.index += 2
            prefix = self.string[:2]
        elif self.string[:3] == "bcc":
            self.index += 3
            prefix = "bcc"
        elif self.string[:4] == "from":
            self.index += 4
            prefix = "from"

        self.chomp_whitespace()

        if self.chomp() != ":":
            raise EmailParseException("no colon ':' in emailPrefix")

        return self.string[: self.index]

    def email_address(self) -> str:
        email_term_regex = re.compile(r"[0-9a-zA-Z_-]+@[0-9a-zA-Z_-]+\.[0-9a-zA-Z_-]+")

        match = email_term_regex.search(self.string)
        if match is not None and match.start() == self.index:
            self.index = match.end()
            # if there are extra characters
            if not self.index == len(self.string):
                raise EmailParseException("Error: extra characters after email")

            return self.string[match.start() : match.end()]

    ############################################################################


class ParseException(Exception):
    pass


class DateParseException(ParseException):
    pass


class EmailParseException(ParseException):
    pass


# test
# p = Parser("date:     2000/11/11")
# idk = p.parse()
# print(idk.date_prefix)
# print(idk.date)

p = Parser("from : abc@x.yz")
idk = p.parse()
print(idk.email_prefix)
print(idk.email_address)
