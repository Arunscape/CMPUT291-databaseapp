import re
import sys
import xml.etree.ElementTree as ElementTree

terms_out = open("terms.txt", "w")
emails_out = open("emails.txt", "w")
dates_out = open("dates.txt", "w")
recs_out = open("recs.txt", "w")

re_terms = re.compile("[0-9a-z_-]+")


def process_terms(row, name, data):
    if data is None or len(data) == 0:
        return

    data = data.lower()
    for term in re.finditer(re_terms, data):
        word = term.group(0)
        if len(word) > 2:
            terms_out.write(name + "-" + word + ":" + row + "\n")


def process_emails(row, name, data):
    if data is not None and len(data) > 0:
        data = data.lower().strip()
        emails_out.write(name + "-" + data + ":" + row + "\n")


def process_dates(row, data):
    if data is not None and len(data) > 0:
        dates_out.write(data.strip() + ":" + row + "\n")


def process_recs(row, data):
    if data is not None and len(data) > 0:
        pass


def process_line(row):
    tree = ElementTree.fromstring(row)
    data = {}
    for child in tree:
        tag = child.tag.lower()
        if tag in data:
            print("Error: Duplicate tag")
            return
        else:
            data[tag] = child.text

    if "row" not in data:
        print("Error: No row number")
        return

    if "subj" in data:
        process_terms(data["row"], "s", data["subj"])
    if "body" in data:
        process_terms(data["row"], "b", data["body"])

    if "from" in data:
        process_emails(data["row"], "from", data["from"])
    if "to" in data:
        process_emails(data["row"], "to", data["to"])
    if "cc" in data:
        process_emails(data["row"], "cc", data["cc"])
    if "bcc" in data:
        process_emails(data["row"], "bcc", data["bcc"])

    if "date" in data:
        process_dates(data["row"], data["date"])

    process_recs(data["row"], row)


for line in sys.stdin:
    line = line.strip()
    if line.startswith("<mail>"):
        process_line(line)

terms_out.close()
emails_out.close()
dates_out.close()
recs_out.close()
