#!/bin/bash
for (( c=1; c<=30; c++ ))
do
     python ./day_update.py $c &
done
