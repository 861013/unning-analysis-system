from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List
from datetime import datetime, timedelta
from bson import ObjectId
import requests
import json

import sys
import os
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_root)

from models.user import User
from utils.database import Database
from app.auth import get_current_user

router = APIRouter(prefix="/api/training-plan", tags=["训练计划"])

# DeepSeek API配置（需要从环境变量获取）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"


async def get_user_history_data(user_id: str, days: int = 30) -> dict:
    """获取用户历史数据"""
    collection = Database.get_collection("exercise")
    
    # 计算日期范围
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 查询数据
    cursor = collection.find({
        "userId": user_id,
        "timestamp": {"$gte": start_date, "$lte": end_date}
    }).sort("timestamp", 1)
    
    exercises = await cursor.to_list(length=None)
    
    # 统计数据
    heart_rates = []
    paces = []
    calories_list = []
    distances = []
    durations = []
    
    for ex in exercises:
        band_data = ex.get("bandData", {}) or {}
        treadmill_data = ex.get("treadmillData", {}) or {}
        
        if band_data.get("heartRate"):
            heart_rates.append(band_data["heartRate"])
        if band_data.get("pace"):
            paces.append(band_data["pace"])
        if band_data.get("calories"):
            calories_list.append(band_data["calories"])
        if treadmill_data.get("distance"):
            distances.append(treadmill_data["distance"])
        if treadmill_data.get("duration"):
            durations.append(treadmill_data["duration"])
    
    # 获取用户基础信息
    user_collection = Database.get_collection("users")
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    
    basic_info = ex.get("basicInfo", {}) or {} if exercises else {}
    if user:
        basic_info.update({
            "gender": user.get("gender"),
            "birthday": user.get("birthday")
        })
    
    return {
        "basic_info": basic_info,
        "heart_rates": heart_rates,
        "paces": paces,
        "calories": calories_list,
        "distances": distances,
        "durations": durations,
        "total_exercises": len(exercises),
        "days": days
    }


def format_prompt_for_deepseek(history_data: dict, plan_type: str, goal: str) -> str:
    """格式化提示词给DeepSeek API"""
    basic_info = history_data.get("basic_info", {})
    heart_rates = history_data.get("heart_rates", [])
    paces = history_data.get("paces", [])
    
    avg_heart_rate = sum(heart_rates) / len(heart_rates) if heart_rates else 0
    avg_pace = sum(paces) / len(paces) if paces else 0
    
    prompt = f"""你是一位专业的跑步训练教练。请根据以下用户数据，生成一份科学的个性化训练计划。

用户基本信息：
- 性别：{basic_info.get('gender', '未知')}
- 年龄：{basic_info.get('age', '未知')}
- 身高：{basic_info.get('height', '未知')}cm
- 体重：{basic_info.get('weight', '未知')}kg
- 体脂率：{basic_info.get('bodyFat', '未知')}%

历史运动数据（最近{history_data.get('days', 30)}天）：
- 训练次数：{history_data.get('total_exercises', 0)}次
- 平均心率：{avg_heart_rate:.1f}bpm
- 平均配速：{avg_pace:.2f}min/km
- 平均卡路里：{sum(history_data.get('calories', [])) / len(history_data.get('calories', [])) if history_data.get('calories') else 0:.0f}kcal

训练目标：{goal}
计划类型：{plan_type}（{'短期计划1-4周' if plan_type == 'short' else '长期计划1-6个月'}）

请生成一份详细的训练计划，包括：
1. 每周训练安排（训练日、休息日）
2. 每次训练的具体内容（热身、主训练、放松）
3. 训练强度（心率区间、配速区间）
4. 训练时长和距离
5. 训练建议和注意事项

请以JSON格式返回，包含以下字段：
- title: 训练计划标题
- duration: 计划时长（周）
- goal: 训练目标
- weekly_schedule: 每周训练安排（数组）
- daily_plans: 每日训练计划（数组）
- suggestions: 训练建议（数组）
"""
    return prompt


async def call_deepseek_api(prompt: str) -> dict:
    """调用DeepSeek API"""
    if not DEEPSEEK_API_KEY:
        # 如果没有API Key，返回模拟数据
        return {
            "title": "个性化训练计划",
            "duration": 4,
            "goal": "提升跑步能力",
            "weekly_schedule": [
                {"week": 1, "training_days": ["周一", "周三", "周五"], "rest_days": ["周二", "周四", "周六", "周日"]}
            ],
            "daily_plans": [
                {
                    "day": "周一",
                    "warmup": "5分钟慢跑",
                    "main": "30分钟中等强度跑步",
                    "cooldown": "5分钟拉伸",
                    "heart_rate_zone": "60-70%",
                    "pace": "6-7 min/km"
                }
            ],
            "suggestions": [
                "保持规律训练",
                "注意休息和恢复",
                "逐步增加训练强度"
            ]
        }
    
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是一位专业的跑步训练教练。"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # 解析AI返回的内容
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # 尝试解析JSON
        try:
            plan_data = json.loads(content)
        except json.JSONDecodeError:
            # 如果不是JSON，返回文本内容
            plan_data = {
                "title": "个性化训练计划",
                "content": content,
                "duration": 4 if "短期" in content else 12
            }
        
        return plan_data
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"调用DeepSeek API失败: {str(e)}"
        )


@router.post("/generate")
async def generate_training_plan(
    plan_type: str = "short",  # short: 1-4周, long: 1-6个月
    goal: str = "improve_pace",  # improve_pace, improve_endurance, lose_weight, etc.
    days: int = 30,
    current_user: dict = Depends(get_current_user)
):
    """生成训练计划"""
    user_id = current_user["id"]
    
    # 获取历史数据
    history_data = await get_user_history_data(user_id, days)
    
    # 格式化提示词
    prompt = format_prompt_for_deepseek(history_data, plan_type, goal)
    
    # 调用DeepSeek API
    plan_data = await call_deepseek_api(prompt)
    
    # 保存训练计划到数据库
    collection = Database.get_collection("training_plans")
    plan_doc = {
        "user_id": user_id,
        "plan_type": plan_type,
        "goal": goal,
        "plan_data": plan_data,
        "history_data_summary": {
            "avg_heart_rate": sum(history_data.get("heart_rates", [])) / len(history_data.get("heart_rates", [])) if history_data.get("heart_rates") else 0,
            "avg_pace": sum(history_data.get("paces", [])) / len(history_data.get("paces", [])) if history_data.get("paces") else 0,
            "total_exercises": history_data.get("total_exercises", 0)
        },
        "created_at": datetime.now(),
        "status": "active"  # active, completed, cancelled
    }
    
    result = await collection.insert_one(plan_doc)
    plan_doc["id"] = str(result.inserted_id)
    
    return {
        "message": "训练计划生成成功",
        "plan_id": plan_doc["id"],
        "plan": plan_data
    }


@router.get("/list")
async def list_training_plans(
    current_user: dict = Depends(get_current_user),
    status_filter: Optional[str] = None
):
    """获取用户的训练计划列表"""
    collection = Database.get_collection("training_plans")
    
    query = {"user_id": current_user["id"]}
    if status_filter:
        query["status"] = status_filter
    
    cursor = collection.find(query).sort("created_at", -1)
    plans = await cursor.to_list(length=100)
    
    result = []
    for plan in plans:
        plan["id"] = str(plan["_id"])
        plan["created_at"] = plan.get("created_at", plan["_id"].generation_time)
        result.append({
            "id": plan["id"],
            "plan_type": plan.get("plan_type"),
            "goal": plan.get("goal"),
            "title": plan.get("plan_data", {}).get("title", "训练计划"),
            "duration": plan.get("plan_data", {}).get("duration", 0),
            "status": plan.get("status"),
            "created_at": plan["created_at"].isoformat() if isinstance(plan["created_at"], datetime) else str(plan["created_at"])
        })
    
    return {"plans": result}


@router.get("/{plan_id}")
async def get_training_plan(
    plan_id: str,
    current_user: dict = Depends(get_current_user)
):
    """获取训练计划详情"""
    collection = Database.get_collection("training_plans")
    plan = await collection.find_one({
        "_id": ObjectId(plan_id),
        "user_id": current_user["id"]
    })
    
    if not plan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="训练计划不存在"
        )
    
    plan["id"] = str(plan["_id"])
    plan["created_at"] = plan.get("created_at", plan["_id"].generation_time)
    
    return {
        "id": plan["id"],
        "plan_type": plan.get("plan_type"),
        "goal": plan.get("goal"),
        "plan_data": plan.get("plan_data"),
        "history_data_summary": plan.get("history_data_summary"),
        "status": plan.get("status"),
        "created_at": plan["created_at"].isoformat() if isinstance(plan["created_at"], datetime) else str(plan["created_at"])
    }

