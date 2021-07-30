#!/bin/bash

count_entries()
{
    printf "Entries    Date \n"
    cat $LOGFILE | cut -d" " -f1 | uniq -c
}

LOGFILE="journal.log"
if [ ! -f $LOGFILE ]; then touch $LOGFILE; 
fi

if [ $1 == "count" ]; then count_entries;
elif [ $1 == "log" ]; then cat $LOGFILE;
else
    message=$@
    when=`date +"%Y-%m-%d %H:%M:%S"`
    echo "$when - $message" >> $LOGFILE
fi
