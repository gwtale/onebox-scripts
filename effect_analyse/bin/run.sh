#!/bin/bash
for (( c=1; c<=35; c++ ))
do
     python ./main.py $c &
done
