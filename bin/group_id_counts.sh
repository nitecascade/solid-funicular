#!/usr/bin/env bash

for i in 0 1 2 3 4 5 6 7 8 9
do
    n=$( find big_data/members_in_group_/${i} -type f -print | wc -l )
    echo "${i},${n}"
done
