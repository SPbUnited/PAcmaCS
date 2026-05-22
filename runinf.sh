#!/bin/env bash


counter=0

while true
do
    echo -e "\033[32mExecuting command '$1': \033[0m'$2'..."
    bash -c "$2"
    echo -e "\033[31mCommand exited:"
    echo $?
    echo -e "\033[0m\033[33m  ==== restarting $counter... ====\033[0m\n"
    counter=$counter+1
    sleep 1
done
