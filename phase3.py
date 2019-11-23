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


def intersect(a, b):
    return [elem for elem in a if elem in b]


def filter_date(operator, date):
    # TODO
    pass


def filter_email(field, email):
    global current_rows

    # Fast path
    if current_rows is not None and len(current_rows) == 0:
        return

    # Normal path
    lookup_string = field + "-" + email
    new_rows = []

    curs = emails_db.cursor()
    entry = curs.get(lookup_string)
    while entry is not None:
        new_rows.append(entry)
        entry = curs.next_dup()

    if current_rows is None:
        current_rows = entry
    else:
        current_rows = intersect(current_rows, new_rows)


def filter_field(field, term, is_prefix):
    # TODO
    pass


def show_records():
    # TODO: Print emails according to current_rows
    print(current_rows)
    pass


def parse(line):
    global output_full, current_rows

    line = line.strip()
    if len(line) == 0:
        return

    # Special commands
    if line == "output=full":
        output_full = True
        return
    if line == "output=brief":
        output_full = False
        return

    # Queries
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

        # Something went wrong, reset
        print("Syntax Error")
        current_rows = None
        return

    # Show results and reset
    show_records()
    current_rows = None


def main():
    print("Email Lookup App")
    print()

    while True:
        command = input("> ")
        parse(command)


if __name__ == "__main__":
    main()
