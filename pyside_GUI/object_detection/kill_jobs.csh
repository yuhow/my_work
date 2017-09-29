#!/bin/csh -f
#
#
# killing job of model-training through GUI (v0)
#
# author: Yoh-Hao Chang
#
# 2017-9-20

set processId_py  = `ps -fu $USER | grep "${1}" | grep "${2}" |grep -v 'grep' | awk '{print $2}'`

if ("$processId_py" != "") then
    foreach processId ($processId_py)
        kill $processId
    end
    
    #echo 'Your job is killed!'
    exit 1
else
    #echo 'Your job doesn't exist!'
    exit 0
endif
