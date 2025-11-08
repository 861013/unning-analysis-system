# 项目结构说明

## 目录结构

```
demo/
├── backend/                    # 后端代码目录
│   ├── app/                    # FastAPI应用目录
│   │   ├── __init__.py         # Python包初始化文件
│   │   ├── main.py             # FastAPI主应用文件
│   │   ├── auth.py             # 认证路由（用户注册、登录、认证）
│   │   ├── video.py            # 视频路由（视频上传、预览、分析）
│   │   └── training_plan.py    # 训练计划路由（AI训练计划生成）
│   ├── models/                 # 数据模型目录
│   │   ├── __init__.py         # Python包初始化文件
│   │   ├── exercise.py         # 运动数据模型定义
│   │   └── user.py             # 用户数据模型定义
│   ├── utils/                  # 工具函数目录
│   │   ├── __init__.py         # Python包初始化文件
│   │   ├── database.py         # MongoDB数据库连接管理
│   │   ├── security.py         # 安全工具（JWT、密码加密）
│   │   └── export.py           # 导出工具（PDF、CSV、JSON）
│   ├── venv/                   # Python虚拟环境（不提交到Git）
│   ├── __init__.py             # Python包初始化文件
│   ├── config.py               # 配置文件
│   ├── main.py                 # 后端服务启动入口
│   └── requirements.txt        # Python依赖列表
│
├── frontend/                   # 前端代码目录
│   ├── css/                    # 样式文件目录
│   │   └── style.css           # 主样式文件
│   ├── js/                     # JavaScript文件目录
│   │   ├── api.js              # API请求封装
│   │   └── app.js              # 前端应用逻辑
│   ├── images/                 # 图片资源目录
│   └── index.html              # 前端主页面
│
├── miniprogram/                # 微信小程序代码目录
│   ├── app.js                  # 小程序入口
│   ├── app.json                # 小程序配置
│   ├── app.wxss                # 全局样式
│   ├── pages/                  # 页面目录
│   │   ├── index/              # 首页
│   │   └── login/              # 登录/注册页
│   ├── utils/                  # 工具函数目录
│   │   └── api.js              # API请求封装
│   ├── components/             # 组件目录
│   └── images/                 # 图片资源目录
│
├── data/                       # 数据文件目录（不提交到Git）
│   └── videos/                 # 视频文件存储目录
│
├── .gitignore                  # Git忽略文件配置
├── README.md                   # 项目说明文档
├── PROJECT_STRUCTURE.md        # 项目结构说明文档（本文件）
├── 启动指南.md                  # 详细启动操作指南
├── 功能实现总结.md              # 功能实现总结
├── 功能对照与优化计划.md        # 功能对照表和优化计划
├── 微信小程序使用指南.md        # 小程序使用指南
├── GitHub提交说明.md           # GitHub提交说明
├── start_backend.sh            # 后端服务启动脚本
└── start_frontend.sh           # 前端服务启动脚本
```

## 文件说明

### 后端文件

#### `backend/app/main.py`
FastAPI主应用文件，包含：
- API路由定义
- CORS中间件配置
- 数据库连接管理
- 数据CRUD操作
- 统计和导出功能

#### `backend/app/auth.py`
认证路由文件，包含：
- 用户注册接口
- 用户登录接口
- 用户信息管理接口
- 账号绑定接口
- JWT Token认证

#### `backend/app/video.py`
视频路由文件，包含：
- 视频上传接口
- 视频列表查询接口
- 视频预览接口
- 视频分析接口（待集成MediaPipe/TensorFlow）

#### `backend/app/training_plan.py`
训练计划路由文件，包含：
- 训练计划生成接口（集成DeepSeek API）
- 训练计划查询接口
- 训练计划详情接口

#### `backend/models/exercise.py`
运动数据模型定义，包含：
- `BasicInfo`: 基础信息模型（性别、年龄、身高、体重等）
- `BandData`: 手环数据模型（心率、配速、卡路里等）
- `TreadmillData`: 跑步机数据模型（速度、坡度、距离等）
- `ExerciseData`: 完整的运动数据模型

#### `backend/models/user.py`
用户数据模型定义，包含：
- `UserCreate`: 用户注册模型
- `UserLogin`: 用户登录模型
- `UserUpdate`: 用户信息更新模型
- `UserBind`: 账号绑定模型
- `User`: 用户模型
- `Token`: Token模型

#### `backend/utils/database.py`
数据库连接管理类，包含：
- MongoDB连接管理
- 数据库和集合获取方法

#### `backend/utils/security.py`
安全工具类，包含：
- JWT Token生成和验证
- 密码加密和验证（bcrypt）
- 用户认证依赖函数

#### `backend/utils/export.py`
导出工具类，包含：
- CSV格式导出
- JSON格式导出
- PDF格式导出（使用reportlab）

#### `backend/main.py`
后端服务启动入口，使用uvicorn启动FastAPI应用。

#### `backend/requirements.txt`
Python依赖包列表：
- fastapi: Web框架
- uvicorn: ASGI服务器
- pymongo: MongoDB驱动
- motor: 异步MongoDB驱动
- pydantic: 数据验证
- python-jose: JWT认证
- passlib: 密码加密
- bcrypt: 密码哈希
- email-validator: 邮箱验证
- requests: HTTP请求（DeepSeek API）
- reportlab: PDF生成
- Pillow: 图像处理
- aiofiles: 异步文件操作
- python-multipart: 文件上传支持
- python-dotenv: 环境变量管理

### 前端文件

#### `frontend/index.html`
前端主页面，包含：
- 数据录入表单
- 数据列表展示
- 数据图表展示
- 数据导出功能

#### `frontend/css/style.css`
前端样式文件，包含：
- 响应式布局
- 标签页样式
- 表单样式
- 数据卡片样式
- 图表容器样式

#### `frontend/js/api.js`
API请求封装，包含：
- API基础配置
- 请求封装函数
- 数据获取函数
- 数据创建函数
- 统计和导出函数

#### `frontend/js/app.js`
前端应用逻辑，包含：
- 标签页切换
- 表单提交处理
- 数据列表加载
- 图表数据加载和渲染
- CSV导出功能

## 技术栈

### 后端
- **Python 3.12.3**: 编程语言
- **FastAPI 0.104.1**: Web框架
- **Uvicorn 0.24.0**: ASGI服务器
- **Motor 3.3.2**: 异步MongoDB驱动
- **Pydantic 2.5.0**: 数据验证

### 前端
- **HTML5**: 页面结构
- **CSS3**: 样式设计
- **JavaScript (ES6+)**: 应用逻辑
- **Chart.js 4.4.0**: 图表库（通过CDN引入）

### 数据库
- **MongoDB**: NoSQL文档数据库

## 数据流

1. **数据录入**: 用户在前端表单输入数据 → 前端通过API发送POST请求 → 后端接收并存储到MongoDB
2. **数据查询**: 前端发送GET请求 → 后端从MongoDB查询数据 → 返回JSON格式数据 → 前端渲染展示
3. **数据统计**: 前端请求统计数据 → 后端聚合MongoDB数据 → 返回统计结果 → 前端绘制图表
4. **数据导出**: 前端请求导出 → 后端查询数据并生成CSV → 返回文件流 → 前端下载文件

## API端点

### 基础URL
```
http://localhost:8000
```

### 端点列表

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | API根路径，返回API信息 |
| GET | `/api/exercise` | 获取运动数据列表 |
| POST | `/api/exercise` | 创建运动数据 |
| GET | `/api/exercise/{id}` | 根据ID获取运动数据 |
| GET | `/api/statistics` | 获取统计数据 |
| GET | `/api/export/csv` | 导出CSV数据 |
| GET | `/api/export/json` | 导出JSON数据 |
| GET | `/api/export/pdf` | 导出PDF数据 |
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| GET | `/api/auth/me` | 获取当前用户信息 |
| PUT | `/api/auth/me` | 更新用户信息 |
| POST | `/api/auth/bind` | 绑定账号 |
| POST | `/api/video/upload` | 上传视频 |
| GET | `/api/video/list` | 获取视频列表 |
| GET | `/api/video/{id}/preview` | 预览视频 |
| POST | `/api/video/{id}/analyze` | 分析视频 |
| POST | `/api/training-plan/generate` | 生成训练计划 |
| GET | `/api/training-plan/list` | 获取训练计划列表 |
| GET | `/api/training-plan/{id}` | 获取训练计划详情 |

## 数据库结构

### 数据库名称
```
running_analysis
```

### 集合名称
- `exercise`: 运动数据集合
- `users`: 用户数据集合
- `videos`: 视频数据集合
- `training_plans`: 训练计划集合

### 文档结构示例
```json
{
  "_id": ObjectId("..."),
  "userId": "user001",
  "timestamp": ISODate("2024-01-15T10:30:00Z"),
  "basicInfo": {
    "gender": "male",
    "age": 28,
    "height": 175,
    "weight": 70,
    "bodyFat": 15
  },
  "bandData": {
    "heartRate": 145,
    "pace": 5.5,
    "calories": 350,
    "trainingLoad": 85
  },
  "treadmillData": {
    "speed": 10.5,
    "incline": 2.0,
    "duration": 30,
    "distance": 5.25
  }
}
```

## 运行流程

1. **启动MongoDB服务**
   ```bash
   sudo systemctl start mongod
   ```

2. **启动后端服务**
   ```bash
   cd demo
   ./start_backend.sh
   ```
   或
   ```bash
   cd backend
   source venv/bin/activate
   python main.py
   ```

3. **启动前端服务**
   ```bash
   cd demo
   ./start_frontend.sh
   ```
   或
   ```bash
   cd frontend
   python3 -m http.server 8080
   ```

4. **访问应用**
   在浏览器中打开: `http://localhost:8080`

