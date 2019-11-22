import re

dateQuery = re.compile(r'^date\s*(:|>|<|>=|<=)\s*([0-9]{4}/[0-9]{2}/[0-9]{2})(?: |$)')
emailQuery = re.compile(
    r'^(from|to|cc|bcc)\s*:\s*([0-9a-zA-Z_-]+(?:\.[0-9a-zA-Z_-]+)*@[0-9a-zA-Z_-]+(?:\.[0-9a-zA-Z_-]+)*)(?: |$)')
termQuery = re.compile(r'^(subj|body|)\s*([0-9a-zA-Z_-]+)(%|)(?: |$)')


def parse(line):
    while len(line) > 0:
        print(line)

        match = dateQuery.match(line)
        if match is not None:
            print("DATE(operator, date) = (", match.group(1), ", ", match.group(2), ")")
            line = line[match.end():]
            continue

        match = emailQuery.match(line)
        if match is not None:
            print("EMAIL(field, email) = (", match.group(1), ", ", match.group(2), ")")
            line = line[match.end():]
            continue

        match = termQuery.match(line)
        if match is not None:
            print("TERM(field, term, end) = (", match.group(1), ", ", match.group(2), ",", match.group(3), ")")
            line = line[len(match.string):]
            continue

        print("Syntax error")
        return

    print("No syntax error, parsing complete")


if __name__ == '__main__':
    parse("date>1999/12/21")
    print()
    parse("from:joe@exmaple.com")
    print()
    parse("subj test%")
    print()
    parse("date  <= 1999/12/21 from     : joe.joe.joe.joe@localhost body hello")
