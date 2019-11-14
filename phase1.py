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


for line in sys.stdin:
    line = line.strip()
    if line.startswith("<mail>"):
        process_line(line)

terms_out.close()
emails_out.close()
dates_out.close()
recs_out.close()
