from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
from bson import ObjectId
import re


class UserCreate(BaseModel):
    """用户注册模型"""
    username: Optional[str] = None  # 昵称
    phone: Optional[str] = None  # 手机号
    email: Optional[EmailStr] = None  # 邮箱
    password: str = Field(..., min_length=6, description="密码，至少6位")
    gender: Optional[str] = None  # 性别：male, female, other
    birthday: Optional[str] = None  # 生日：YYYY-MM-DD格式
    avatar: Optional[str] = None  # 头像URL

    @validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('手机号格式不正确')
        return v

    @validator('phone', 'email', pre=True, always=True)
    def validate_contact(cls, v, values):
        # 至少提供手机号或邮箱之一
        phone = values.get('phone')
        email = values.get('email')
        if not phone and not email:
            raise ValueError('必须提供手机号或邮箱')
        return v


class UserLogin(BaseModel):
    """用户登录模型"""
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    wechat_openid: Optional[str] = None  # 微信OpenID（小程序登录）

    @validator('password')
    def validate_password(cls, v, values):
        # 微信登录不需要密码
        if not values.get('wechat_openid') and not v:
            raise ValueError('必须提供密码或微信OpenID')
        return v


class UserUpdate(BaseModel):
    """用户信息更新模型"""
    username: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    avatar: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None


class UserBind(BaseModel):
    """账号绑定模型"""
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    wechat_openid: Optional[str] = None
    verification_code: Optional[str] = None  # 验证码（可选）


class User(BaseModel):
    """用户模型"""
    id: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    wechat_openid: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    avatar: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    is_active: bool = True

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }


class Token(BaseModel):
    """Token模型"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1小时


class UserProfile(BaseModel):
    """用户资料模型（不包含敏感信息）"""
    id: str
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    avatar: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        json_encoders = {
            ObjectId: str,
            datetime: lambda v: v.isoformat()
        }

