#!/bin/bash

# A single script to run multiple OpenAI Gym environments
# within one single file, instead of multiple consoles.
# It receives the environment ID and the number of instances
# to be created, numbers start at 0.
# https://unix.stackexchange.com/questions/55558/how-can-i-kill-and-wait-for-background-processes-to-finish-in-a-shell-script-whe


if [ "$#" -ne 2 ]
then
      echo "This script needs two arguments, Gym env ID and number of instances"
      exit 1
fi

if [ "$2" -le 0 ]
then
      echo "It needs a positive number of instances"
      exit 1
fi

finish()
{
    procs="$(jobs -p)"
    echo "Kill: $procs"
    # Ignore process that are already dead
    kill $procs 2> /dev/null
}

PYCMD="python3 gym-uds-server.py"
SOCKPATH="unix://tmp/gym-uds-socket"

for (( i=0; i<$2; i++ ))
do
   $PYCMD $1 $SOCKPATH$i &
done

trap 'finish' 2
echo 'Press <Ctrl+C> to kill...'
wait