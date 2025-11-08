#!/bin/bash

# GitHub上传脚本
# 仓库地址: https://github.com/861013/unning-analysis-system

echo "=========================================="
echo "开始上传项目到GitHub"
echo "仓库地址: https://github.com/861013/unning-analysis-system"
echo "=========================================="
echo ""

# 检查是否在demo目录
if [ ! -f "README.md" ]; then
    echo "错误：请在demo目录下执行此脚本"
    echo "请先执行: cd demo"
    exit 1
fi

# 步骤1: 初始化Git仓库
echo "步骤1: 初始化Git仓库..."
if [ -d ".git" ]; then
    echo "⚠️  Git仓库已存在，跳过初始化"
else
    git init
    echo "✅ Git仓库初始化完成"
fi
echo ""

# 步骤2: 检查.gitignore文件
echo "步骤2: 检查.gitignore文件..."
if [ -f ".gitignore" ]; then
    echo "✅ .gitignore文件已存在"
else
    echo "⚠️  警告：.gitignore文件不存在"
fi
echo ""

# 步骤3: 添加所有文件
echo "步骤3: 添加文件到暂存区..."
git add .
echo "✅ 文件已添加到暂存区"
echo ""

# 步骤4: 查看状态
echo "步骤4: 查看当前状态..."
git status
echo ""

# 步骤5: 提交到本地仓库
echo "步骤5: 提交到本地仓库..."
read -p "请输入提交信息（直接回车使用默认信息）: " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="初始提交：跑步分析系统项目

- 完整的项目代码（后端、前端、小程序）
- 项目文档（功能总结、启动指南等）
- 技术栈：Python + FastAPI + MongoDB
- 功能：数据采集、分析、可视化、训练计划生成"
fi

git commit -m "$commit_msg"
echo "✅ 提交完成"
echo ""

# 步骤6: 添加远程仓库
echo "步骤6: 添加远程仓库..."
if git remote | grep -q "origin"; then
    echo "⚠️  远程仓库origin已存在，正在更新..."
    git remote set-url origin https://github.com/861013/unning-analysis-system.git
else
    git remote add origin https://github.com/861013/unning-analysis-system.git
fi
echo "✅ 远程仓库已添加"
echo ""

# 步骤7: 验证远程仓库地址
echo "步骤7: 验证远程仓库地址..."
git remote -v
echo ""

# 步骤8: 设置主分支
echo "步骤8: 设置主分支为main..."
git branch -M main
echo "✅ 主分支已设置为main"
echo ""

# 步骤9: 推送到GitHub
echo "步骤9: 推送到GitHub..."
echo "⚠️  注意：如果提示输入用户名和密码，请使用Personal Access Token（不是GitHub密码）"
echo ""
read -p "按回车键继续推送，或按Ctrl+C取消..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ 上传成功！"
    echo "=========================================="
    echo "仓库地址: https://github.com/861013/unning-analysis-system"
    echo "您可以在浏览器中访问该地址查看您的代码"
else
    echo ""
    echo "=========================================="
    echo "❌ 推送失败"
    echo "=========================================="
    echo "可能的原因："
    echo "1. 需要身份验证（请使用Personal Access Token）"
    echo "2. 网络连接问题"
    echo "3. 远程仓库权限问题"
    echo ""
    echo "请检查错误信息并重试"
fi

