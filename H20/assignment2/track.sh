#!/bin/bash

track() 
{
    LOGFILE=~/.local/share/track.log
    HELPFUL_MSG="ERROR: Run with argument \"start\", \"stop\", \"status\" or \"log\""
    
    if [ -s ${LOGFILE} ]; then  # logfile exists and is not empty
        last=`cat ${LOGFILE} | tail -n 1 | cut -d" " -f1`
        if [ ${last} == "END" ]; then
            running=false
        else
            running=true
        fi
    elif [ -f ${LOGFILE} ]; then # logfile exists but is empty
        running=false
    else    # logfile does not exist
        echo Creating logfile: ${LOGFILE}
        touch ${LOGFILE}
        running=false
    fi
    
    if [ $# -eq 0 ]; then
        echo ${HELPFUL_MSG}
        return 1
    fi
    option=$1;
    shift;
    case "$option" in 
        "start")
            start $@; ;;
        "stop")
            stop; ;;
        "status")
            status; ;;
        "log")
            display_log; ;;
        *)
            echo ${HELPFUL_MSG}; return 1 ;;
    esac
}

start()
{
    if [ $# -eq 0 ]; then
        echo "Include label with start: track start [label]"
        return 1
    elif $running; then
        printf "ERROR: Cannot start task.\nA task is already running.\n"
        return 1
    fi
    label=$@
    echo "" >> ${LOGFILE}
    echo "START `date`" >> ${LOGFILE}
    echo "LABEL ${label}" >> ${LOGFILE}
    echo "Task started: ${label}";
}

stop()
{
    if ! ${running}; then
        printf "ERROR: Cannot stop task.\nNo task is running.\n"
        return 1
    fi
    echo "END `date`" >> ${LOGFILE}
    echo "Task stopped"
}

status()
{
    if $running; then
        echo Task running:
        cat $LOGFILE | tail -n 2
    else
        echo No task is running.
    fi
}

display_log()
{
    declare -i task_counter=1
    while read -r line; do
        read -r line
        starttime=`echo $line | cut -d" " -f5`

        read -r line
        label=`echo $line | cut -d" " -f2-`

        read -r line
        stoptime=`echo $line | cut -d" " -f5`

        diff=`time_diff $starttime $stoptime`
        echo "Task ${task_counter}: ${diff}, ${label}"
        (( task_counter++ ))
    done < $LOGFILE
}

time_diff()
{
    declare -i starttime=`HMS_to_seconds $1`
    declare -i stoptime=`HMS_to_seconds $2`
    declare -i diff=$(( stoptime - starttime ))
    seconds_to_HMS $diff
}

HMS_to_seconds()
{
    H=`echo $1 | cut -d":" -f1`
    M=`echo $1 | cut -d":" -f2`
    S=`echo $1 | cut -d":" -f3`
    H=$((10#$H))    # Handle leading zeros in the numbers
    M=$((10#$M))
    S=$((10#$S))
    seconds=$(( $H*3600 + $M*60 + $S ))
    echo $seconds
}

seconds_to_HMS()
{
    declare -i seconds=$1
    declare -i S=$(( $seconds % 60 ))
    declare -i minutes=$(( $seconds / 60 ))
    declare -i M=$(( $minutes % 60 ))
    declare -i H=$(( $minutes / 60 ))
    printf "%02d:%02d:%02d\n" $H $M $S
}

