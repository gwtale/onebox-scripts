#!/bin/bash
for (( c=1; c<=30; c++ ))
do
     python ./main.py $c &
done
