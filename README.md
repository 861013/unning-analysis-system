# 跑步分析系统

> 基于NoSQL数据库的智能跑步分析系统 - 整合多设备数据，提供数据采集、分析、可视化、训练计划生成等功能

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Community-brightgreen.svg)](https://www.mongodb.com/)
[![License](https://img.shields.io/badge/License-Open%20Source-blue.svg)](LICENSE)

---

## 📖 项目简介

跑步分析系统是一个基于设计思维流程开发的智能运动数据分析平台。系统整合多设备数据（小米手环10、体脂秤S400、跑步机），提供数据采集、存储、分析、可视化、训练计划生成等功能，支持Web端和微信小程序端。

### 核心特性

- 🎯 **多设备数据整合** - 统一管理来自不同设备的运动数据
- 📊 **智能数据分析** - 多维度数据分析和趋势可视化
- 🤖 **AI训练计划** - 集成DeepSeek API生成个性化训练计划
- 📹 **视频姿势分析** - 支持多角度视频上传和姿势分析（待完善）
- 📱 **跨平台支持** - Web端和微信小程序端，数据实时同步
- 🔐 **完整用户系统** - 用户注册、登录、认证、账号绑定

---

## ✨ 主要功能

### 1. 数据采集与存储
- ✅ 手动数据录入（基础信息、运动数据）
- ✅ 数据验证和格式化（Pydantic验证）
- ✅ MongoDB文档型数据库存储
- ⚠️ 文件上传（CSV/JSON导入）待实现

### 2. 数据分析与可视化
- ✅ 数据查询和筛选
- ✅ 基础图表展示（折线图、柱状图）
- ✅ 统计信息（平均值、最大值、最小值）
- ✅ 趋势分析

### 3. 训练计划生成（AI集成）
- ✅ DeepSeek API集成
- ✅ 短期训练计划（1-4周）
- ✅ 长期训练计划（1-6个月）
- ✅ 基于历史数据的个性化生成
- ✅ 训练计划导出（PDF/CSV/JSON）

### 4. 视频姿势分析
- ✅ 多角度视频上传（正面、侧面、后面）
- ✅ 视频预览和列表查询
- ⚠️ 姿势识别和分析（待集成MediaPipe/TensorFlow）

### 5. 用户管理系统
- ✅ 用户注册/登录（支持手机号/邮箱/微信）
- ✅ 用户信息管理（昵称、头像、性别、生日）
- ✅ 账号绑定（手机号、邮箱、微信互相绑定）
- ✅ JWT Token认证和自动刷新

### 6. 数据导出
- ✅ CSV格式导出
- ✅ JSON格式导出
- ✅ PDF格式导出

### 7. 微信小程序端
- ✅ 用户登录/注册
- ✅ 首页（用户信息、统计数据展示）
- ✅ API请求封装和Token管理
- ✅ 数据同步（与Web端共享API）
- ⚠️ 数据录入、列表、图表页面功能待完善

---

## 🛠️ 技术栈

### 后端技术
- **运行时**: Python 3.12
- **Web框架**: FastAPI 0.104.1
- **数据库**: MongoDB Community Edition
- **异步驱动**: Motor 3.3.2
- **认证**: JWT (python-jose)
- **密码加密**: bcrypt (passlib)
- **AI集成**: DeepSeek API
- **PDF生成**: reportlab

### 前端技术
- **基础**: HTML5 + CSS3 + JavaScript
- **图表库**: Chart.js
- **响应式**: Bootstrap
- **HTTP请求**: Fetch API

### 小程序技术
- **框架**: 微信小程序原生框架
- **UI库**: WeUI
- **图表库**: wx-charts

**所有技术均为开源免费，无任何商业限制。**

---

## 📁 项目结构

```
demo/
├── backend/                    # 后端代码
│   ├── app/                   # FastAPI应用
│   │   ├── main.py            # 主应用
│   │   ├── auth.py            # 认证路由
│   │   ├── video.py           # 视频路由
│   │   └── training_plan.py   # 训练计划路由
│   ├── models/                # 数据模型
│   │   ├── user.py           # 用户模型
│   │   └── exercise.py         # 运动数据模型
│   ├── utils/                 # 工具函数
│   │   ├── database.py        # 数据库连接
│   │   ├── security.py        # 安全工具（JWT、密码加密）
│   │   └── export.py          # 导出工具
│   ├── venv/                  # Python虚拟环境（不提交到Git）
│   ├── requirements.txt       # Python依赖
│   └── main.py                # 启动入口
├── frontend/                  # 前端代码
│   ├── index.html             # 主页面
│   ├── css/                   # 样式文件
│   ├── js/                    # JavaScript文件
│   └── images/                # 图片资源
├── miniprogram/               # 微信小程序代码
│   ├── app.js                 # 小程序入口
│   ├── app.json               # 小程序配置
│   ├── pages/                 # 页面目录
│   └── utils/                  # 工具函数
├── data/                      # 数据文件（不提交到Git）
├── start_backend.sh           # 后端启动脚本
├── start_frontend.sh          # 前端启动脚本
├── README.md                  # 本文件
├── PROJECT_STRUCTURE.md       # 项目结构说明
├── 启动指南.md                 # 详细启动指南
├── 功能实现总结.md             # 功能实现总结
├── 功能对照与优化计划.md       # 功能对照和优化计划
└── 微信小程序使用指南.md        # 小程序使用指南
```

---

## 🚀 快速开始

### 环境要求

- Python 3.12+
- MongoDB 4.4+
- 现代浏览器（Chrome、Firefox、Edge等）

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/您的用户名/仓库名.git
cd 仓库名
```

#### 2. 启动MongoDB服务

```bash
# 检查MongoDB服务状态
sudo systemctl status mongod

# 如果未运行，启动服务
sudo systemctl start mongod

# 设置开机自启（可选）
sudo systemctl enable mongod
```

#### 3. 配置后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 4. 配置环境变量（可选）

创建`.env`文件：

```bash
# MongoDB配置
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=running_analysis

# DeepSeek API配置（可选）
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# JWT密钥（生产环境必须修改）
SECRET_KEY=your-secret-key-change-in-production
```

#### 5. 启动服务

**启动后端：**

```bash
./start_backend.sh
```

或手动启动：

```bash
cd backend
source venv/bin/activate
python main.py
```

后端服务将在 `http://localhost:8000` 启动。

**启动前端：**

```bash
./start_frontend.sh
```

或手动启动：

```bash
cd frontend
python3 -m http.server 8080
```

前端服务将在 `http://localhost:8080` 启动。

#### 6. 访问应用

在浏览器中打开：`http://localhost:8080`

---

## 📚 文档

- [启动指南.md](启动指南.md) - 详细启动操作指南
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - 项目结构说明
- [功能实现总结.md](功能实现总结.md) - 功能实现总结
- [功能对照与优化计划.md](功能对照与优化计划.md) - 功能对照表和优化计划
- [微信小程序使用指南.md](微信小程序使用指南.md) - 小程序使用指南

---

## 📊 项目完成度

| 模块 | 完成度 | 说明 |
|------|--------|------|
| 数据采集与存储 | 60% | 手动录入已实现，文件上传待实现 |
| 视频姿势分析 | 51.4% | 上传和预览已实现，分析功能待集成 |
| 数据分析与可视化 | 57.5% | 基础功能已实现，高级功能待完善 |
| 训练计划生成 | 81.8% | DeepSeek API集成完成，编辑功能待完善 |
| 数据导出 | 90% | CSV/JSON/PDF全部实现 |
| 用户管理 | 87.5% | 完整实现，数据隐私设置待实现 |
| 微信小程序端 | 52.5% | 基础结构完成，页面功能待完善 |
| **总体完成度** | **70.5%** | 核心功能基本完成 |

---

## 🔧 API接口

### 认证相关
- `POST /api/auth/register` - 用户注册
- `POST /api/auth/login` - 用户登录
- `GET /api/auth/me` - 获取当前用户信息
- `PUT /api/auth/me` - 更新用户信息
- `POST /api/auth/bind` - 绑定账号

### 运动数据
- `GET /api/exercise` - 获取运动数据列表
- `POST /api/exercise` - 提交运动数据
- `GET /api/exercise/{id}` - 获取单条运动数据
- `GET /api/statistics` - 获取统计数据

### 视频分析
- `POST /api/video/upload` - 上传视频
- `GET /api/video/list` - 获取视频列表
- `GET /api/video/{id}/preview` - 预览视频
- `POST /api/video/{id}/analyze` - 分析视频

### 训练计划
- `POST /api/training-plan/generate` - 生成训练计划
- `GET /api/training-plan/list` - 获取训练计划列表
- `GET /api/training-plan/{id}` - 获取训练计划详情

### 数据导出
- `GET /api/export/csv` - 导出CSV数据
- `GET /api/export/json` - 导出JSON数据
- `GET /api/export/pdf` - 导出PDF数据

详细API文档请访问：`http://localhost:8000/docs`（Swagger UI）

---

## 🎯 项目特点

1. **开源免费** - 所有技术栈均为开源免费软件
2. **跨平台兼容** - 支持Ubuntu 24和Windows 11系统
3. **AI集成** - 集成DeepSeek API实现智能训练计划生成
4. **多端支持** - Web端和小程序端共享后端API
5. **完整认证** - JWT Token认证，密码加密存储
6. **设计思维** - 基于设计思维流程开发，注重用户体验

---

## 📝 开发计划

### 第一优先级（必须实现）
- [ ] 完善小程序端页面功能（数据录入、列表、图表、训练计划）
- [ ] 集成视频分析库（MediaPipe或TensorFlow）
- [ ] 实现文件上传功能（CSV/JSON导入）
- [ ] 完善数据筛选功能（日期范围、多条件）

### 第二优先级（重要功能）
- [ ] 实现训练计划编辑功能
- [ ] 实现训练计划执行跟踪
- [ ] 完善数据可视化（热力图、对比图表）
- [ ] 实现数据隐私设置

### 第三优先级（可选功能）
- [ ] 高级数据可视化（3D图表）
- [ ] 性能优化（缓存、索引）
- [ ] 安全性增强（HTTPS、限流）

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

## 📄 许可证

本项目采用开源许可证，所有技术栈均为开源免费软件。

---

## 👥 作者

**开发团队**

| 姓名 | 学号 | 负责部分 |
|------|------|----------|
| *** | ***** | PPT制作 |
| *** | ***** | 演讲汇报 |
| *** | ***** | PPT制作 |
| *** | ***** | 撰写报告 |

---

## 🙏 致谢

感谢所有参与项目开发的团队成员，感谢在开发过程中提供帮助和支持的老师和同学。

---

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交Issue: [GitHub Issues](https://github.com/您的用户名/仓库名/issues)

---

**⭐ 如果这个项目对您有帮助，请给个Star支持一下！**
