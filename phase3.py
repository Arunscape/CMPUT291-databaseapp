#! /usr/bin/env python3

from bsddb3 import db

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

def tokenize(s: str)
    for c in s:
        if c != ' ':
            yield c
    while True:
        yield '\0'

@dataclass
class Node:
    left: Node
    right: Node
    name: Node

    def debug(n: Node):
        s: str = '['
        if n.left != None:
            s += debug(n.left)
        
        s += f" {n.name} "
        
        if n.right != None:
            s += debug(n.right)
        return f"{s} ]"

class Parser:

    def __init__(self, s):
        self.lexer = lexer(s)
        self.curr = next(self.lexer)

    def alphanumeric(self) -> Node:
        l = self.curr
        self.curr = next(self.lexer)

        if l.isalnum():
            print("Expected an alphanumeric sequence")
            return None

        return Node(None, None, 1)
    
    def numeric(self) -> Node:
        l = self.curr
        self.curr = next(self.lexer)

        if l.isnumeric():
            print("Expected a numeric sequence")
            return None
        return Node(None, None, 1)

    # date            ::= numeric numeric numeric numeric '/' numeric numeric '/' numeric numeric
    def date(self) -> Node:
        l = self.numeric()
        self.curr = next(self.lexer)

        if l == None:
            return None
        pass

    def datePrefix(self) -> Node:
        pass
    def dateQuery(self) -> Node:
        pass
    def emailterm(self) -> Node:
        pass
    def email(self) -> Node:
        pass
    def emailPrefix(self) -> Node:
        pass
    def emailQuery(self) -> Node:
        pass
    def term(self) -> Node:
        pass
    def termPrefix(self) -> Node:
        pass
    def termSuffix(self) -> Node:
        pass
    def termQuery(self) -> Node:
        pass
    def expression(self) -> Node:
        pass
    def query(self) -> Node:
        pass
    def modeChange(self) -> Node:
        pass
    def command(self) -> Node:
        pass
