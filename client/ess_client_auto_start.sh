#!/bin/bash

str=$"\n"

cd /home/weitao/ess-vue-django/client
npm install
npm run build
nohup node server.js > /dev/null 2>&1 &

sstr=$(echo -e $str)
echo $sstr