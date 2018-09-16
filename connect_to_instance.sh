#!/bin/bash
if [ $1 == "server1" ]; then
    host=118.27.7.140
elif [ $1 == "server2" ]; then
    host=118.27.11.242
elif [ $1 == "server3" ]; then
    host=118.27.0.245
else
    host=118.27.7.140
fi

exec ssh isucon@$host
