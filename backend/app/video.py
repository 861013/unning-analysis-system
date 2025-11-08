from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
import os
import aiofiles

import sys
import os as os_module
backend_root = os_module.path.dirname(os_module.path.dirname(os_module.path.abspath(__file__)))
sys.path.insert(0, backend_root)

from utils.database import Database
from app.auth import get_current_user

router = APIRouter(prefix="/api/video", tags=["视频"])
UPLOAD_DIR = os.path.join(os_module.path.dirname(os_module.path.dirname(os_module.path.dirname(backend_root))), "data", "videos")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# 允许的视频格式
ALLOWED_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    angle: str = "front",  # front, side, back
    current_user: dict = Depends(get_current_user)
):
    """上传视频文件"""
    # 检查文件扩展名
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件格式。支持的格式：{', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # 检查角度
    if angle not in ["front", "side", "back"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角度必须是 front、side 或 back"
        )
    
    # 读取文件内容
    content = await file.read()
    
    # 检查文件大小
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制（最大{MAX_FILE_SIZE // 1024 // 1024}MB）"
        )
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{current_user['id']}_{angle}_{timestamp}{file_ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    # 保存文件
    async with aiofiles.open(filepath, 'wb') as f:
        await f.write(content)
    
    # 保存视频信息到数据库
    collection = Database.get_collection("videos")
    video_data = {
        "user_id": current_user["id"],
        "filename": filename,
        "filepath": filepath,
        "angle": angle,
        "original_filename": file.filename,
        "file_size": len(content),
        "uploaded_at": datetime.now(),
        "analysis_status": "pending",  # pending, processing, completed, failed
        "analysis_result": None
    }
    
    result = await collection.insert_one(video_data)
    video_data["id"] = str(result.inserted_id)
    
    return {
        "message": "视频上传成功",
        "video_id": video_data["id"],
        "filename": filename,
        "angle": angle,
        "file_size": len(content)
    }


@router.get("/list")
async def list_videos(
    current_user: dict = Depends(get_current_user),
    angle: Optional[str] = None
):
    """获取用户的视频列表"""
    collection = Database.get_collection("videos")
    
    query = {"user_id": current_user["id"]}
    if angle:
        query["angle"] = angle
    
    cursor = collection.find(query).sort("uploaded_at", -1)
    videos = await cursor.to_list(length=100)
    
    result = []
    for video in videos:
        video["id"] = str(video["_id"])
        video["uploaded_at"] = video.get("uploaded_at", video["_id"].generation_time)
        result.append({
            "id": video["id"],
            "filename": video.get("filename"),
            "original_filename": video.get("original_filename"),
            "angle": video.get("angle"),
            "file_size": video.get("file_size"),
            "uploaded_at": video["uploaded_at"].isoformat() if isinstance(video["uploaded_at"], datetime) else str(video["uploaded_at"]),
            "analysis_status": video.get("analysis_status", "pending"),
            "analysis_result": video.get("analysis_result")
        })
    
    return {"videos": result}


@router.get("/{video_id}/preview")
async def preview_video(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """预览视频"""
    collection = Database.get_collection("videos")
    video = await collection.find_one({
        "_id": ObjectId(video_id),
        "user_id": current_user["id"]
    })
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="视频不存在"
        )
    
    filepath = video.get("filepath")
    if not os.path.exists(filepath):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="视频文件不存在"
        )
    
    # 返回视频文件流
    async def generate():
        async with aiofiles.open(filepath, 'rb') as f:
            while True:
                chunk = await f.read(8192)
                if not chunk:
                    break
                yield chunk
    
    return StreamingResponse(
        generate(),
        media_type="video/mp4",
        headers={
            "Content-Disposition": f'inline; filename="{video.get("original_filename", "video.mp4")}"'
        }
    )


@router.post("/{video_id}/analyze")
async def analyze_video(
    video_id: str,
    current_user: dict = Depends(get_current_user)
):
    """分析视频姿势（占位符，实际需要集成MediaPipe或TensorFlow）"""
    collection = Database.get_collection("videos")
    video = await collection.find_one({
        "_id": ObjectId(video_id),
        "user_id": current_user["id"]
    })
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="视频不存在"
        )
    
    # 更新分析状态
    await collection.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": {
            "analysis_status": "processing",
            "updated_at": datetime.now()
        }}
    )
    
    # TODO: 这里应该集成MediaPipe或TensorFlow进行姿势分析
    # 目前返回模拟结果
    analysis_result = {
        "score": 85,
        "knee_alignment": "good",
        "foot_strike": "midfoot",
        "arm_swing": "optimal",
        "posture": "upright",
        "suggestions": [
            "保持当前姿势",
            "注意保持身体直立",
            "适当增加步频"
        ],
        "key_points": []  # 关键点坐标
    }
    
    # 更新分析结果
    await collection.update_one(
        {"_id": ObjectId(video_id)},
        {"$set": {
            "analysis_status": "completed",
            "analysis_result": analysis_result,
            "updated_at": datetime.now()
        }}
    )
    
    return {
        "message": "视频分析完成",
        "analysis_result": analysis_result
    }

