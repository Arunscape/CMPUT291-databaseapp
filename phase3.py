#!/usr/bin/env python3
import re
from bsddb3 import db

output_full = False
current_rows = None


def open_db(file, mode):
    database = db.DB()
    database.open(file, None, mode)
    return database


recs_db = open_db("re.idx", db.DB_HASH)
terms_db = open_db("te.idx", db.DB_BTREE)
emails_db = open_db("em.idx", db.DB_BTREE)
dates_db = open_db("da.idx", db.DB_BTREE)

re_date_query = re.compile(
    r"^date\s*(:|>|<|>=|<=)\s*([0-9]{4}/[0-9]{2}/[0-9]{2})(?:\s+|$)"
)
re_email_query = re.compile(
    r"^(from|to|cc|bcc)\s*:\s*([0-9a-zA-Z_-]+(?:\.[0-9a-zA-Z_-]+)*@[0-9a-zA-Z_-]+(?:\.[0-9a-zA-Z_-]+)*)(?:\s+|$)"
)
re_term_query = re.compile(r"^(subj|body|)\s*([0-9a-zA-Z_-]+)(%|)(?:\s+|$)")


def filter_date(operator, date):
    pass


def filter_email(field, email):
    pass


def filter_field(field, term, is_prefix):
    pass


def show_records():
    # Print emails according to current_rows
    pass


def parse(line):
    global output_full, current_rows

    line = line.strip()
    if line == "output=full":
        output_full = True
        return
    if line == "output=brief":
        output_full = False
        return

    while len(line) > 0:
        match = re_date_query.match(line)
        if match is not None:
            filter_date(match.group(1), match.group(2))
            line = line[match.end() :]
            continue

        match = re_email_query.match(line)
        if match is not None:
            filter_email(match.group(1), match.group(2))
            line = line[match.end() :]
            continue

        match = re_term_query.match(line)
        if match is not None:
            filter_field(match.group(1), match.group(2), match.group(3) == "%")
            line = line[match.end() :]
            continue

        print("Syntax Error")
        current_rows = None
        return

    show_records()


def main():
    print("Email Lookup App")
    print()

    while True:
        command = input("> ")
        parse(command)


if __name__ == "__main__":
    main()
