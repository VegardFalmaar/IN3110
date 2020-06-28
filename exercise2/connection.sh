#!/bin/bash

ping -c1 google.com > /dev/null 2>&1
if [ "$?" == "0" ]; then
    echo Connected
else
    echo Not connected
fi
