from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class BasicInfo(BaseModel):
    """基础信息模型"""
    gender: Optional[str] = None
    age: Optional[int] = None
    height: Optional[float] = None  # cm
    weight: Optional[float] = None  # kg
    bodyFat: Optional[float] = None  # %
    muscleMass: Optional[float] = None  # kg
    waterContent: Optional[float] = None  # %


class SleepData(BaseModel):
    """睡眠数据模型"""
    duration: Optional[float] = None  # hours
    deepSleep: Optional[float] = None
    lightSleep: Optional[float] = None
    remSleep: Optional[float] = None


class BandData(BaseModel):
    """手环数据模型"""
    heartRate: Optional[int] = None  # bpm
    pace: Optional[float] = None  # min/km
    trainingLoad: Optional[int] = None
    calories: Optional[int] = None
    sleep: Optional[SleepData] = None


class TreadmillData(BaseModel):
    """跑步机数据模型"""
    speed: Optional[float] = None  # km/h
    incline: Optional[float] = None  # %
    duration: Optional[int] = None  # minutes
    distance: Optional[float] = None  # km


class ExerciseDataCreate(BaseModel):
    """创建运动数据模型"""
    userId: str = Field(default="user001", description="用户ID")
    basicInfo: Optional[BasicInfo] = None
    bandData: Optional[BandData] = None
    treadmillData: Optional[TreadmillData] = None


class ExerciseData(ExerciseDataCreate):
    """运动数据模型（包含ID和时间戳）"""
    id: Optional[str] = None
    timestamp: Optional[datetime] = None

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

