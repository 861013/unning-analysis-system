#!/bin/bash

# GitHub代码推送脚本
# 仓库地址: https://github.com/861013/unning-analysis-system

echo "=========================================="
echo "GitHub代码推送助手"
echo "仓库地址: https://github.com/861013/unning-analysis-system"
echo "=========================================="
echo ""

# 检查是否在demo目录
if [ ! -f "README.md" ]; then
    echo "错误：请在demo目录下执行此脚本"
    echo "请先执行: cd /home/hadoop/nosql/run/demo"
    exit 1
fi

# 检查Git仓库
if [ ! -d ".git" ]; then
    echo "错误：当前目录不是Git仓库"
    exit 1
fi

# 检查远程仓库
if ! git remote | grep -q "origin"; then
    echo "错误：未配置远程仓库"
    exit 1
fi

echo "步骤1: 检查当前状态..."
git status
echo ""

echo "步骤2: 查看提交历史..."
git log --oneline -3
echo ""

echo "步骤3: 配置身份验证..."
echo ""
echo "请选择身份验证方式："
echo "1. 使用Personal Access Token（推荐）"
echo "2. 使用SSH密钥（如果已配置）"
echo ""
read -p "请输入选项 (1 或 2): " auth_method

if [ "$auth_method" = "1" ]; then
    echo ""
    echo "请按照以下步骤创建Personal Access Token："
    echo "1. 访问: https://github.com/settings/tokens"
    echo "2. 点击 'Generate new token' → 'Generate new token (classic)'"
    echo "3. 填写信息并勾选 'repo' 权限"
    echo "4. 点击 'Generate token'"
    echo "5. 复制生成的token（只显示一次）"
    echo ""
    read -p "请输入您的Personal Access Token: " token
    
    if [ -z "$token" ]; then
        echo "错误：Token不能为空"
        exit 1
    fi
    
    echo ""
    echo "正在更新远程仓库URL..."
    git remote set-url origin https://861013:${token}@github.com/861013/unning-analysis-system.git
    echo "✅ 远程仓库URL已更新"
    
elif [ "$auth_method" = "2" ]; then
    echo ""
    echo "检查SSH密钥..."
    if [ -f ~/.ssh/id_ed25519.pub ] || [ -f ~/.ssh/id_rsa.pub ]; then
        echo "✅ 检测到SSH密钥"
        git remote set-url origin git@github.com:861013/unning-analysis-system.git
        echo "✅ 已切换到SSH方式"
    else
        echo "❌ 未检测到SSH密钥"
        echo "请先配置SSH密钥，或选择方式1使用Token"
        exit 1
    fi
else
    echo "错误：无效的选项"
    exit 1
fi

echo ""
echo "步骤4: 推送到GitHub..."
echo ""

# 尝试推送
if git push -u origin main; then
    echo ""
    echo "=========================================="
    echo "✅ 推送成功！"
    echo "=========================================="
    echo "仓库地址: https://github.com/861013/unning-analysis-system"
    echo "您可以在浏览器中访问该地址查看您的代码"
else
    echo ""
    echo "=========================================="
    echo "❌ 推送失败"
    echo "=========================================="
    echo "可能的原因："
    echo "1. Token无效或已过期"
    echo "2. 网络连接问题"
    echo "3. 远程仓库权限问题"
    echo ""
    echo "请检查错误信息并重试"
    exit 1
fi

