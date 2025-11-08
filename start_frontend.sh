#!/bin/bash
# 前端服务启动脚本

cd "$(dirname "$0")/frontend"

# 启动HTTP服务器
echo "正在启动前端服务..."
echo "请在浏览器中访问: http://localhost:8080"
python3 -m http.server 8080

