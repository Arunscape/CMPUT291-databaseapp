#!/bin/bash

set -e
set -u

# For testing only, do not submit

function do_diff {
    echo '----- ----- -----'
    set +e
    diff -u "$1" "$2"
    set -e
    echo '----- ----- -----'
}

function test_one {
    local PREFIX=./data${1}/${1}
    python3 phase1.py < "${PREFIX}".xml

    echo 'terms.txt diff:'
    do_diff terms.txt "${PREFIX}"-terms.txt

    echo 'emails.txt diff:'
    do_diff emails.txt "${PREFIX}"-emails.txt

    echo 'dates.txt diff:'
    do_diff dates.txt "${PREFIX}"-dates.txt

    echo 'recs.txt diff:'
    do_diff recs.txt "${PREFIX}"-recs.txt

    # shellcheck disable=SC2162
    read -p 'Press enter to continue...'
}

test_one 10
test_one 1k

make clean
