#!/bin/bash
# run_sendall.sh - 每 10 秒执行一次 SendALL.py

while true
do
    /usr/bin/python3 /www/wwwroot/default/WechatTest/SendALL.py >> /www/wwwroot/default/WechatTest/logs/send_all.log 2>&1
    sleep 10
done
