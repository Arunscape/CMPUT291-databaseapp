#!/usr/bin/env python3
import re
from bsddb3 import db


re_date_query = re.compile(r"^date\s*(:|>|<|>=|<=)\s*([0-9]{4}/[0-9]{2}/[0-9]{2})(?:\s+|$)")
re_email_query = re.compile(
    r"^(from|to|cc|bcc)\s*:\s*([0-9a-zA-Z_-]+(?:\.[0-9a-zA-Z_-]+)*@[0-9a-zA-Z_-]+(?:\.[0-9a-zA-Z_-]+)*)(?:\s+|$)"
)
re_term_query = re.compile(r"^(subj|body|)\s*([0-9a-zA-Z_-]+)(%|)(?:\s+|$)")


def parse(line):
    while len(line) > 0:
        match = re_date_query.match(line)
        if match is not None:
            print("DATE(operator, date) = (", match.group(1), ", ", match.group(2), ")")
            line = line[match.end() :]
            continue

        match = re_email_query.match(line)
        if match is not None:
            print("EMAIL(field, email) = (", match.group(1), ", ", match.group(2), ")")
            line = line[match.end() :]
            continue

        match = re_term_query.match(line)
        if match is not None:
            print(
                "TERM(field?, term, end?) = (",
                match.group(1),
                ", ",
                match.group(2),
                ",",
                match.group(3),
                ")",
            )
            line = line[match.end() :]
            continue

        print("Syntax error")
        return

    print("No syntax error, parsing complete")


def main() :
    print("Email Lookup App")
    print()

    while True:
        command = input("> ")
        parse(command)


if __name__ == "__main__":
    main()
