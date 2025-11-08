#!/bin/bash
# 后端服务启动脚本

cd "$(dirname "$0")/backend"

# 激活虚拟环境
source venv/bin/activate

# 启动服务
echo "正在启动后端服务..."
python main.py

