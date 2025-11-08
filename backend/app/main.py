from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from datetime import datetime
from bson import ObjectId
import csv
import io
from typing import List, Optional

import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_root)

from models.exercise import ExerciseData, ExerciseDataCreate
from utils.database import Database
from app.auth import router as auth_router
from app.video import router as video_router
from app.training_plan import router as training_plan_router
from app.auth import get_current_user
from utils.export import export_to_csv, export_to_json, export_to_pdf

app = FastAPI(title="跑步分析系统API", version="2.0.0")

# 注册路由
app.include_router(auth_router)
app.include_router(video_router)
app.include_router(training_plan_router)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """应用启动时连接数据库"""
    await Database.connect()


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时断开数据库连接"""
    await Database.disconnect()


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "跑步分析系统API",
        "version": "2.0.0",
        "endpoints": {
            "认证相关": {
                "POST /api/auth/register": "用户注册",
                "POST /api/auth/login": "用户登录",
                "GET /api/auth/me": "获取当前用户信息",
                "PUT /api/auth/me": "更新用户信息",
                "POST /api/auth/bind": "绑定账号",
                "POST /api/auth/send-verification-code": "发送验证码"
            },
            "运动数据": {
                "GET /api/exercise": "获取运动数据列表",
                "POST /api/exercise": "提交运动数据",
                "GET /api/exercise/{id}": "获取单条运动数据",
                "GET /api/statistics": "获取统计数据"
            },
            "视频分析": {
                "POST /api/video/upload": "上传视频",
                "GET /api/video/list": "获取视频列表",
                "GET /api/video/{id}/preview": "预览视频",
                "POST /api/video/{id}/analyze": "分析视频"
            },
            "训练计划": {
                "POST /api/training-plan/generate": "生成训练计划",
                "GET /api/training-plan/list": "获取训练计划列表",
                "GET /api/training-plan/{id}": "获取训练计划详情"
            },
            "数据导出": {
                "GET /api/export/csv": "导出CSV数据",
                "GET /api/export/json": "导出JSON数据",
                "GET /api/export/pdf": "导出PDF数据"
            }
        }
    }


@app.get("/api/exercise", response_model=List[ExerciseData])
async def get_exercise_data(
    userId: Optional[str] = None,
    limit: int = 100,
    skip: int = 0
):
    """获取运动数据列表"""
    collection = Database.get_collection("exercise")
    
    query = {}
    if userId:
        query["userId"] = userId
    
    cursor = collection.find(query).sort("timestamp", -1).skip(skip).limit(limit)
    results = await cursor.to_list(length=limit)
    
    exercise_list = []
    for doc in results:
        doc["id"] = str(doc["_id"])
        doc["timestamp"] = doc.get("timestamp", doc.get("_id").generation_time)
        exercise_list.append(ExerciseData(**doc))
    
    return exercise_list


@app.post("/api/exercise", response_model=ExerciseData)
async def create_exercise_data(exercise: ExerciseDataCreate):
    """创建运动数据"""
    collection = Database.get_collection("exercise")
    
    exercise_dict = exercise.dict()
    exercise_dict["timestamp"] = datetime.now()
    
    result = await collection.insert_one(exercise_dict)
    
    # 获取插入的文档
    inserted_doc = await collection.find_one({"_id": result.inserted_id})
    inserted_doc["id"] = str(inserted_doc["_id"])
    inserted_doc["timestamp"] = inserted_doc.get("timestamp", inserted_doc["_id"].generation_time)
    
    return ExerciseData(**inserted_doc)


@app.get("/api/exercise/{exercise_id}", response_model=ExerciseData)
async def get_exercise_by_id(exercise_id: str):
    """根据ID获取运动数据"""
    collection = Database.get_collection("exercise")
    
    try:
        doc = await collection.find_one({"_id": ObjectId(exercise_id)})
        if not doc:
            raise HTTPException(status_code=404, detail="运动数据未找到")
        
        doc["id"] = str(doc["_id"])
        doc["timestamp"] = doc.get("timestamp", doc["_id"].generation_time)
        return ExerciseData(**doc)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"无效的ID格式: {str(e)}")


@app.get("/api/statistics")
async def get_statistics(userId: Optional[str] = None):
    """获取统计数据"""
    collection = Database.get_collection("exercise")
    
    query = {}
    if userId:
        query["userId"] = userId
    
    cursor = collection.find(query)
    results = await cursor.to_list(length=None)
    
    if not results:
        return {
            "heartRate": {"avg": 0, "max": 0, "min": 0, "data": []},
            "pace": {"avg": 0, "max": 0, "min": 0, "data": []},
            "calories": {"avg": 0, "max": 0, "min": 0, "data": []},
            "dates": []
        }
    
    heart_rates = []
    paces = []
    calories_list = []
    dates = []
    
    for doc in results:
        timestamp = doc.get("timestamp", doc["_id"].generation_time)
        if isinstance(timestamp, datetime):
            dates.append(timestamp.strftime("%Y-%m-%d"))
        else:
            dates.append(str(timestamp))
        
        if "bandData" in doc and doc["bandData"]:
            if "heartRate" in doc["bandData"] and doc["bandData"]["heartRate"]:
                heart_rates.append(doc["bandData"]["heartRate"])
            if "pace" in doc["bandData"] and doc["bandData"]["pace"]:
                paces.append(doc["bandData"]["pace"])
            if "calories" in doc["bandData"] and doc["bandData"]["calories"]:
                calories_list.append(doc["bandData"]["calories"])
    
    def calc_stats(values):
        if not values:
            return {"avg": 0, "max": 0, "min": 0, "data": []}
        return {
            "avg": round(sum(values) / len(values), 2),
            "max": max(values),
            "min": min(values),
            "data": values
        }
    
    return {
        "heartRate": calc_stats(heart_rates),
        "pace": calc_stats(paces),
        "calories": calc_stats(calories_list),
        "dates": dates[:len(heart_rates)] if heart_rates else dates
    }


@app.get("/api/export/csv")
async def export_csv(
    userId: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """导出CSV数据"""
    collection = Database.get_collection("exercise")
    
    # 如果未指定userId，使用当前用户ID
    if not userId:
        userId = current_user["id"]
    
    query = {"userId": userId}
    
    cursor = collection.find(query).sort("timestamp", -1)
    results = await cursor.to_list(length=None)
    
    # 格式化数据
    data = []
    for doc in results:
        timestamp = doc.get("timestamp", doc["_id"].generation_time)
        if isinstance(timestamp, datetime):
            date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            date_str = str(timestamp)
        
        band_data = doc.get("bandData", {}) or {}
        treadmill_data = doc.get("treadmillData", {}) or {}
        basic_info = doc.get("basicInfo", {}) or {}
        
        data.append({
            "日期": date_str,
            "用户ID": doc.get("userId", ""),
            "心率(bpm)": band_data.get("heartRate", ""),
            "配速(min/km)": band_data.get("pace", ""),
            "卡路里(kcal)": band_data.get("calories", ""),
            "速度(km/h)": treadmill_data.get("speed", ""),
            "距离(km)": treadmill_data.get("distance", ""),
            "时长(分钟)": treadmill_data.get("duration", ""),
            "身高(cm)": basic_info.get("height", ""),
            "体重(kg)": basic_info.get("weight", ""),
            "体脂率(%)": basic_info.get("bodyFat", "")
        })
    
    return await export_to_csv(data, "running_data.csv")


@app.get("/api/export/json")
async def export_json(
    userId: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """导出JSON数据"""
    collection = Database.get_collection("exercise")
    
    # 如果未指定userId，使用当前用户ID
    if not userId:
        userId = current_user["id"]
    
    query = {"userId": userId}
    
    cursor = collection.find(query).sort("timestamp", -1)
    results = await cursor.to_list(length=None)
    
    # 格式化数据
    data = []
    for doc in results:
        doc["id"] = str(doc["_id"])
        doc["timestamp"] = doc.get("timestamp", doc["_id"].generation_time)
        if isinstance(doc["timestamp"], datetime):
            doc["timestamp"] = doc["timestamp"].isoformat()
        doc.pop("_id", None)
        data.append(doc)
    
    return await export_to_json(data, "running_data.json")


@app.get("/api/export/pdf")
async def export_pdf(
    userId: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """导出PDF数据"""
    collection = Database.get_collection("exercise")
    
    # 如果未指定userId，使用当前用户ID
    if not userId:
        userId = current_user["id"]
    
    query = {"userId": userId}
    
    cursor = collection.find(query).sort("timestamp", -1)
    results = await cursor.to_list(length=None)
    
    # 格式化数据
    data = []
    for doc in results:
        timestamp = doc.get("timestamp", doc["_id"].generation_time)
        if isinstance(timestamp, datetime):
            date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            date_str = str(timestamp)
        
        band_data = doc.get("bandData", {}) or {}
        treadmill_data = doc.get("treadmillData", {}) or {}
        basic_info = doc.get("basicInfo", {}) or {}
        
        data.append({
            "日期": date_str,
            "用户ID": doc.get("userId", ""),
            "心率(bpm)": str(band_data.get("heartRate", "")),
            "配速(min/km)": str(band_data.get("pace", "")),
            "卡路里(kcal)": str(band_data.get("calories", "")),
            "速度(km/h)": str(treadmill_data.get("speed", "")),
            "距离(km)": str(treadmill_data.get("distance", "")),
            "时长(分钟)": str(treadmill_data.get("duration", "")),
            "身高(cm)": str(basic_info.get("height", "")),
            "体重(kg)": str(basic_info.get("weight", "")),
            "体脂率(%)": str(basic_info.get("bodyFat", ""))
        })
    
    return await export_to_pdf(data, "运动数据导出", "running_data.pdf")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

