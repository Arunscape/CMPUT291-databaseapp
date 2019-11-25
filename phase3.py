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
terms_curs = terms_db.cursor()

emails_db = open_db("em.idx", db.DB_BTREE)
emails_curs = emails_db.cursor()

dates_db = open_db("da.idx", db.DB_BTREE)
dates_curs = dates_db.cursor()

re_date_query = re.compile(
    r"^date\s*(:|>|<|>=|<=)\s*([0-9]{4}/[0-9]{2}/[0-9]{2})(?:\s+|$)"
)
re_email_query = re.compile(
    r"^(from|to|cc|bcc)\s*:\s*([0-9a-zA-Z_-]+(?:\.[0-9a-zA-Z_-]+)*@[0-9a-zA-Z_-]+(?:\.[0-9a-zA-Z_-]+)*)(?:\s+|$)"
)
re_term_query = re.compile(r"^(subj|body|)\s*:\s*([0-9a-zA-Z_-]+)(%|)(?:\s+|$)")

re_extract_title = re.compile(r"<subj>(.*?)</subj>")


def update_current_rows(new_rows):
    global current_rows

    if current_rows is None:
        current_rows = new_rows
    else:
        current_rows = [elem for elem in new_rows if elem in current_rows]


def filter_date_equal_helper(date, new_rows):
    entry = dates_curs.current()
    while entry is not None and str(entry[0].decode("utf-8")) == date:
        new_rows.append(entry[1])
        entry = dates_curs.next()


def filter_date_less_than(date, allow_equal):
    new_rows = []

    entry = dates_curs.first()
    while entry is not None and str(entry[0].decode("utf-8")) < date:
        new_rows.append(entry[1])
        entry = dates_curs.next()

    if allow_equal and entry is not None:
        filter_date_equal_helper(date, new_rows)

    return new_rows


def filter_date_larger_than(date, allow_equal):
    new_rows = []

    entry = dates_curs.last()
    while entry is not None and str(entry[0].decode("utf-8")) > date:
        new_rows.append(entry[1])
        entry = dates_curs.prev()

    if allow_equal and entry is not None:
        filter_date_equal_helper(date, new_rows)

    return new_rows


def filter_date_equal_only(date):
    new_rows = []

    entry = dates_curs.set(date.encode("utf-8"))
    if entry is not None:
        filter_date_equal_helper(date, new_rows)

    return new_rows


def filter_date(operator, date):
    global current_rows

    # Fast path
    if current_rows is not None and len(current_rows) == 0:
        return

    # Normal path
    if operator == "<":
        new_rows = filter_date_less_than(date, False)
    elif operator == "<=":
        new_rows = filter_date_less_than(date, True)
    elif operator == ">":
        new_rows = filter_date_larger_than(date, False)
    elif operator == ">=":
        new_rows = filter_date_larger_than(date, True)
    else:
        new_rows = filter_date_equal_only(date)

    update_current_rows(new_rows)


def filter_email(field, email):
    global current_rows

    # Fast path
    if current_rows is not None and len(current_rows) == 0:
        return

    # Normal path
    lookup_string = field + "-" + email
    new_rows = []

    entry = emails_curs.set(lookup_string.encode("utf-8"))
    while entry is not None:
        new_rows.append(entry[1])
        entry = emails_curs.next_dup()

    update_current_rows(new_rows)


def filter_field_one(field, term, is_prefix):
    lookup_string = ("b" if field == "body" else "s") + "-" + term
    new_rows = []

    if is_prefix:
        entry = terms_curs.set_range(lookup_string.encode("utf-8"))
        while entry is not None and str(entry[0].decode("utf-8")).startswith(
            lookup_string
        ):
            new_rows.append(entry[1])
            entry = terms_curs.next()
    else:
        entry = terms_curs.set(lookup_string.encode("utf-8"))
        while entry is not None:
            new_rows.append(entry[1])
            entry = terms_curs.next_dup()

    return new_rows


def filter_field(field, term, is_prefix):
    global current_rows

    # Fast path
    if current_rows is not None and len(current_rows) == 0:
        return

    # Normal path
    if field == "":
        new_rows = filter_field_one("subj", term, is_prefix) + filter_field_one(
            "body", term, is_prefix
        )
    else:
        new_rows = filter_field_one(field, term, is_prefix)

    update_current_rows(new_rows)


def show_records():
    global current_rows

    for row in current_rows:
        record = str(recs_db.get(row).decode("utf-8"))
        if output_full:
            print(row.decode("utf-8") + ":" + record)
        else:
            match = re_extract_title.search(record)
            title = "" if match is None else match.group(1)
            print(row.decode("utf-8") + ":" + title)


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
    print("Press Ctrl+C to exit")
    print()

    try:
        while True:
            command = input("> ")
            parse(command.lower())
    except KeyboardInterrupt:
        pass

    print()
    print()
    print("See you next time!")

    recs_db.close()

    terms_curs.close()
    terms_db.close()

    emails_curs.close()
    emails_db.close()

    dates_curs.close()
    dates_db.close()


main()
