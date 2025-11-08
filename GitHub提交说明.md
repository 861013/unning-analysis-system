# GitHub提交说明

本文档说明如何将demo文件夹提交到GitHub。

---

## 📋 提交前准备

### 1. 确保只提交demo文件夹

本项目只提交`demo`文件夹的内容，不提交上级目录的文件。

### 2. 检查.gitignore文件

确保`.gitignore`文件已正确配置，排除以下内容：
- 虚拟环境（venv/）
- 数据文件（data/）
- 环境变量文件（.env）
- 视频文件（*.mp4等）
- 敏感信息（*.key等）

---

## 🚀 提交步骤

### 步骤1：在GitHub上创建新仓库

1. 访问 [https://github.com](https://github.com) 并登录
2. 点击右上角的 **"+"** 按钮，选择 **"New repository"**
3. 填写仓库信息：
   - **Repository name**: 例如 `running-analysis-system`
   - **Description**: 例如 `基于NoSQL数据库的跑步分析系统`
   - **Visibility**: 选择 Public 或 Private
   - **不要勾选**任何初始化选项
4. 点击 **"Create repository"**
5. 复制仓库地址（例如：`https://github.com/您的用户名/仓库名.git`）

### 步骤2：初始化Git仓库

```bash
cd demo
git init
```

### 步骤3：添加文件

```bash
# 添加所有文件（.gitignore会自动排除不需要的文件）
git add .

# 查看将要提交的文件
git status
```

### 步骤4：提交到本地仓库

```bash
git commit -m "初始提交：跑步分析系统项目

- 完整的项目代码（后端、前端、小程序）
- 项目文档（功能总结、启动指南等）
- 技术栈：Python + FastAPI + MongoDB
- 功能：数据采集、分析、可视化、训练计划生成"
```

### 步骤5：连接远程仓库

```bash
# 添加远程仓库地址（替换为您的实际地址）
git remote add origin https://github.com/您的用户名/仓库名.git

# 验证远程仓库地址
git remote -v
```

### 步骤6：推送到GitHub

```bash
# 设置主分支为main
git branch -M main

# 推送到GitHub
git push -u origin main
```

**注意：** 如果提示输入密码，请使用Personal Access Token（不是GitHub密码）。

---

## 🔐 身份验证

如果推送时提示输入用户名和密码：

1. **用户名**：您的GitHub用户名
2. **密码**：使用Personal Access Token

### 如何创建Personal Access Token：

1. 登录GitHub
2. 点击右上角头像 → **Settings**
3. 左侧菜单选择 **Developer settings**
4. 选择 **Personal access tokens** → **Tokens (classic)**
5. 点击 **Generate new token** → **Generate new token (classic)**
6. 填写信息：
   - **Note**: 例如 `本地开发`
   - **Expiration**: 选择过期时间
   - **Select scopes**: 至少勾选 `repo`（完整仓库访问权限）
7. 点击 **Generate token**
8. **立即复制生成的token**（只显示一次）
9. 在Git推送时，密码处粘贴这个token

---

## 📝 后续更新

以后修改代码后，使用以下命令更新：

```bash
# 添加修改的文件
git add .

# 提交修改
git commit -m "更新说明：描述本次修改的内容"

# 推送到GitHub
git push
```

---

## ⚠️ 注意事项

1. **不要提交敏感信息**：
   - `.env`文件（已在.gitignore中排除）
   - API密钥
   - 密码
   - 个人信息

2. **不要提交大文件**：
   - 视频文件（已在.gitignore中排除）
   - 数据库文件
   - 虚拟环境

3. **检查提交内容**：
   - 提交前使用`git status`检查要提交的文件
   - 确保没有提交不应该提交的文件

---

## ✅ 提交检查清单

- [ ] GitHub账号已登录
- [ ] 新仓库已创建
- [ ] 本地Git仓库已初始化
- [ ] .gitignore文件已配置
- [ ] 所有文件已添加到暂存区
- [ ] 首次提交已完成
- [ ] 远程仓库地址已添加
- [ ] Personal Access Token已创建（如果需要）
- [ ] 代码已成功推送到GitHub
- [ ] GitHub仓库页面可以正常查看文件

---

**祝您提交成功！** 🎉

