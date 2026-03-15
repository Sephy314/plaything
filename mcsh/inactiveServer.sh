#!/bin/bash

SERVER_DIR=~/yaseng
SERVER_JAR="server.jar"

# PID 찾기
PID=$(ps aux | grep "[${SERVER_JAR:0:1}]${SERVER_JAR:1}" | awk '{print $2}')

if [ -z "$PID" ]; then
    echo "서버 꺼짐 ❌"
    exit 0
fi

# 안전하게 종료
kill -SIGTERM "$PID"

# 최대 10초 대기하며 종료 확인
for i in {1..10}; do
    if ps -p "$PID" > /dev/null 2>&1; then
        sleep 1
    else
        echo "서버 종료 완료 ✅"
        exit 0
    fi
done

# 여전히 살아있으면 강제 종료
kill -9 "$PID" 2>/dev/null
echo "서버 강제 종료 ⚠️ (PID: $PID)"
exit 0