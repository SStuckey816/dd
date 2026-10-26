#!/bin/bash
while true 
do 
    dig @172.28.10.2 -p 53 cs.uic.edu
    sleep 10
done