from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from datetime import datetime, timedelta
from bson import ObjectId

import sys
import os
backend_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_root)

from models.user import UserCreate, UserLogin, User, Token, UserUpdate, UserBind
from utils.database import Database
from utils.security import (
    verify_password, get_password_hash, create_access_token,
    decode_access_token, generate_verification_code
)

router = APIRouter(prefix="/api/auth", tags=["认证"])
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """获取当前用户"""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
        )
    
    # 从数据库获取用户信息
    collection = Database.get_collection("users")
    user = await collection.find_one({"_id": ObjectId(user_id)})
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
        )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )
    
    user["id"] = str(user["_id"])
    return user


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate):
    """用户注册"""
    collection = Database.get_collection("users")
    
    # 检查手机号或邮箱是否已存在
    query = {}
    if user_data.phone:
        query["phone"] = user_data.phone
    if user_data.email:
        query["email"] = user_data.email
    
    if query:
        existing_user = await collection.find_one({"$or": [{"phone": user_data.phone}, {"email": user_data.email}]})
        if existing_user:
            if existing_user.get("phone") == user_data.phone:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该手机号已被注册"
                )
            if existing_user.get("email") == user_data.email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="该邮箱已被注册"
                )
    
    # 创建用户
    user_dict = {
        "username": user_data.username,
        "phone": user_data.phone,
        "email": user_data.email,
        "password_hash": get_password_hash(user_data.password),
        "gender": user_data.gender,
        "birthday": user_data.birthday,
        "avatar": user_data.avatar,
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_active": True,
        "wechat_openid": None
    }
    
    result = await collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    user_dict["_id"] = result.inserted_id
    
    # 移除敏感信息
    user_dict.pop("password_hash", None)
    
    return User(**user_dict)


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    """用户登录"""
    collection = Database.get_collection("users")
    
    # 构建查询条件
    query = {}
    if login_data.phone:
        query["phone"] = login_data.phone
    elif login_data.email:
        query["email"] = login_data.email
    elif login_data.wechat_openid:
        query["wechat_openid"] = login_data.wechat_openid
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="必须提供手机号、邮箱或微信OpenID"
        )
    
    user = await collection.find_one(query)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 微信登录不需要密码验证
    if login_data.wechat_openid:
        if user.get("wechat_openid") != login_data.wechat_openid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="微信账号未绑定"
            )
    else:
        # 验证密码
        if not verify_password(login_data.password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户名或密码错误"
            )
    
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )
    
    # 生成Token
    access_token = create_access_token(data={"sub": str(user["_id"])})
    
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息"""
    # 移除敏感信息
    current_user.pop("password_hash", None)
    return User(**current_user)


@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """更新当前用户信息"""
    collection = Database.get_collection("users")
    
    update_data = user_update.dict(exclude_unset=True)
    
    # 如果更新手机号或邮箱，检查是否已被使用
    if update_data.get("phone") or update_data.get("email"):
        query = {"_id": {"$ne": ObjectId(current_user["id"])}}
        or_conditions = []
        if update_data.get("phone"):
            or_conditions.append({"phone": update_data["phone"]})
        if update_data.get("email"):
            or_conditions.append({"email": update_data["email"]})
        if or_conditions:
            query["$or"] = or_conditions
            existing_user = await collection.find_one(query)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="手机号或邮箱已被使用"
                )
    
    update_data["updated_at"] = datetime.now()
    
    await collection.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$set": update_data}
    )
    
    # 获取更新后的用户信息
    updated_user = await collection.find_one({"_id": ObjectId(current_user["id"])})
    updated_user["id"] = str(updated_user["_id"])
    updated_user.pop("password_hash", None)
    
    return User(**updated_user)


@router.post("/bind", response_model=User)
async def bind_account(
    bind_data: UserBind,
    current_user: dict = Depends(get_current_user)
):
    """绑定账号（手机号、邮箱、微信）"""
    collection = Database.get_collection("users")
    
    update_data = {}
    
    # 绑定手机号
    if bind_data.phone:
        # 检查手机号是否已被使用
        existing_user = await collection.find_one({
            "phone": bind_data.phone,
            "_id": {"$ne": ObjectId(current_user["id"])}
        })
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该手机号已被绑定"
            )
        update_data["phone"] = bind_data.phone
    
    # 绑定邮箱
    if bind_data.email:
        # 检查邮箱是否已被使用
        existing_user = await collection.find_one({
            "email": bind_data.email,
            "_id": {"$ne": ObjectId(current_user["id"])}
        })
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被绑定"
            )
        update_data["email"] = bind_data.email
    
    # 绑定微信
    if bind_data.wechat_openid:
        # 检查微信OpenID是否已被使用
        existing_user = await collection.find_one({
            "wechat_openid": bind_data.wechat_openid,
            "_id": {"$ne": ObjectId(current_user["id"])}
        })
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该微信账号已被绑定"
            )
        update_data["wechat_openid"] = bind_data.wechat_openid
    
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="请提供要绑定的账号信息"
        )
    
    update_data["updated_at"] = datetime.now()
    
    await collection.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$set": update_data}
    )
    
    # 获取更新后的用户信息
    updated_user = await collection.find_one({"_id": ObjectId(current_user["id"])})
    updated_user["id"] = str(updated_user["_id"])
    updated_user.pop("password_hash", None)
    
    return User(**updated_user)


@router.post("/send-verification-code")
async def send_verification_code(phone: Optional[str] = None, email: Optional[str] = None):
    """发送验证码（可选功能，用于绑定账号时提高稳定性）"""
    # 这里应该集成短信或邮件服务
    # 目前返回模拟的验证码（生产环境应通过短信/邮件发送）
    code = generate_verification_code()
    
    # 存储验证码到Redis或数据库（这里简化处理）
    # 实际应该存储验证码，设置过期时间（如5分钟）
    
    return {
        "message": "验证码已发送",
        "code": code  # 开发环境返回，生产环境不应返回
    }

