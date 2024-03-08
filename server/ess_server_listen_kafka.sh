#!/bin/bash

str=$"\n"

cd /home/weitao/ess-vue-django/server
nohup /home/weitao/anaconda3/bin/python manage.py listenkfk --start_listen_kafka > /dev/null 2>&1 &

sstr=$(echo -e $str)
echo $sstr