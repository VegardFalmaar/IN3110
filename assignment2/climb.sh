#!/bin/bash

climb () {
  if [ $1 ]; then
    myString=$(printf "%${1}s")
    cd ${myString// /"../"}
  else
    cd ..
  fi
}