import sys
import xml.etree.ElementTree as ElementTree

terms_out = open("terms.txt", "w")
emails_out = open("emails.txt", "w")
dates_out = open("dates.txt", "w")
recs_out = open("recs.txt", "w")


def process_line(line):
    tree = ElementTree.fromstring(line)
    root = tree.getroot()
    for child in root:
        print(child)


for line in sys.stdin:
    line = line.strip()
    if line.startswith("<mail>"):
        process_line(line)

terms_out.close()
emails_out.close()
dates_out.close()
recs_out.close()
