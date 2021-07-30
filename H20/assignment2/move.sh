#!/bin/bash

move () {
    if [ $# -lt 2 ]; then
        echo "Pass at least \"src\" and \"dst\" as arguments"
        return 1
    fi

    if [ "$1" == "-d" ]; then
        date=true
        shift 1
    else
        date=false
    fi

    if [ $# -eq 2 ]; then
        src=$1
        dst=$2
        type="*"
    elif [ $# -eq 3 ]; then
        src=$1
        dst=$2
        type="*.$3"
    fi

    if [ ! -d $src ]; then
        echo "${src} is not a directory"
        return 1
    elif [ ! -d $dst ]; then
        echo "${dst} is not a directory"
        return 1
    fi

    for fname in ${src}/${type}; do
        if [ -d $fname ]; then
            echo Leaving directory $fname alone
        elif [ "${date}" = true ]; then
            folder="${dst}/`date +%F-%H-%M`/"
            echo Moving ${fname} to ${folder}
            if ! [ -d $folder ]; then
                mkdir $folder
            fi
            mv ${fname} ${folder}
        else
            echo Moving ${fname} to ${dst}
            mv ${fname} ${dst}
        fi
    done
}
