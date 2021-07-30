#!/bin/bash

printf "Name: "
read name

declare -i age
printf "Age: "
read age

words=`echo $name | wc -w`
letters=`echo $name | tr -d " \n\r" | wc -m`

echo
echo Name: $name
echo Words: $words
echo Letters: $letters
echo

if [ $age -lt 10 ]; then
    echo $name will be young in 10 years
elif [ $age -lt 50 ]; then
    echo $name will be middle aged in 10 years
else
    echo $name will be old in 10 years
fi
