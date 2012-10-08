#!/bin/bash
for (( c=1; c<=10; c++ ))
do
     python ./main.py $c &
done
