#!/bin/bash

set -e
set -u

rm -f re.idx
rm -f te.idx
rm -f em.idx
rm -f da.idx

sort -u recs.txt   | perl break.pl | db_load -T -t hash re.idx &
sort -u terms.txt  | perl break.pl | db_load -c duplicates=1 -T -t btree te.idx &
sort -u emails.txt | perl break.pl | db_load -c duplicates=1 -T -t btree em.idx &
sort -u dates.txt  | perl break.pl | db_load -c duplicates=1 -T -t btree da.idx &

wait
