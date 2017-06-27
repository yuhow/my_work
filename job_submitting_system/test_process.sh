#!/bin/bash

inner_counter=0

if [ -f "my_job_log.txt" ]
then
    rm -f my_job_log.txt
    touch my_job_log.txt
else
    touch my_job_log.txt
fi

while [ ${inner_counter} -lt 10 ]
do
    if [ ${inner_counter} -lt 10 ]
    then
        echo "HAHA" >> my_job_log.txt
        sleep 1
        inner_counter=$((inner_counter+1))
    fi
    if [ ${inner_counter} -eq 10 ]
    then
        echo "process complete" >> my_job_log.txt
    fi
done
