#!/bin/bash

set -e
set -u

rm -f re.idx
rm -f te.idx
rm -f em.idx
rm -f da.idx

sort -u recs.txt | ./break.pl | db_load -T -t hash re.idx
sort -u terms.txt | ./break.pl | db_load -c duplicates=1 -T -t btree te.idx
sort -u emails.txt | ./break.pl | db_load -c duplicates=1 -T -t btree em.idx
sort -u dates.txt | ./break.pl | db_load -c duplicates=1 -T -t btree da.idx