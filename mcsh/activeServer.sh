#!/bin/bash

SERVER_DIR=~/yaseng

SERVER_JAR="server.jar"


if [ ! -d "$SERVER_DIR" ]; then
    echo "Directory Not Found Exception"
    exit 1
fi

PID=$(ps aux | grep "[${SERVER_JAR:0:1}]${SERVER_JAR:1}" | awk '{print $2}')
if [ -z "$PID" ]; then
    echo "서버 꺼짐 ❌"
else
    echo "서버 켜짐 ✅ (PID: $PID)"
    exit 1
fi

cd "$SERVER_DIR" || { echo "Failed to cd into server directory"; exit 1; }

nohup java -Xmx5G -Xms5G -XX:+UseG1GC -XX:MaxGCPauseMillis=200 -XX:+ParallelRefProcEnabled -jar server.jar nogui
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "Server started successfully ✅"
else
    echo "Server failed to start ❌ (Exit code: $EXIT_CODE)"
fi

exit $EXIT_CODE
