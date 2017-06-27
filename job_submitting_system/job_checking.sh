#!/bin/bash

#################################
# 2017-06-17                    #
# You-Hao Chang                 #
#                               #
# checking job remotely         #
#                               #
# version: v0                   #
#                               #
#################################

# user name
user=echo $USER

# job name which will be monitored
job_name=${1}

# complete command to submit jobs
job_command=${2}

# absolute path of job's log file
job_log_file=${3}

# termination condition
# 1) while the key word "completed" appears in the log file:
termination_key="completed"

condition=""
while [ ${condition} -eq ${termination_key} ]
do
    

done
