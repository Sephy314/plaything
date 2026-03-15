#!/bin/bash

SERVER_JAR="server.jar"

# PID 찾기
PID=$(ps aux | grep "[${SERVER_JAR:0:1}]${SERVER_JAR:1}" | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "서버 꺼짐 ❌"
    exit 0
else
    echo "서버 켜짐 ✅ (PID: $PID)"
    exit 1
fi