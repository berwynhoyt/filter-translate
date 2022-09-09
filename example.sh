#!/bin/bash
#Translate all .d files in subfolders from dutch .de files in english, skipping lines starting with 'macro' or containing «text»

files="$@"
[[ "$files" == "" ]] && files=`find -name "*.d"`

IFS=$'\n'
for i in $files; do
    [ -f "$i"e ] && echo "$i - already done" && continue
    echo "$i "
    filter-translate.py -s nl --filter="-^macro|«.*»" "$i" "$i"e
done
