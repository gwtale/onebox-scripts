#!/bin/bash
for (( c=1; c<=35; c++ ))
do
     python ./day_update.py $c &
     sleep 3
done
