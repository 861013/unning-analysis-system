from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Database:
    """数据库连接管理类"""
    client: Optional[AsyncIOMotorClient] = None
    database = None

    @classmethod
    async def connect(cls):
        """连接到MongoDB"""
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        db_name = os.getenv("MONGODB_DB_NAME", "running_analysis")
        
        cls.client = AsyncIOMotorClient(mongodb_url)
        cls.database = cls.client[db_name]
        print(f"✅ 已连接到MongoDB: {mongodb_url}/{db_name}")

    @classmethod
    async def disconnect(cls):
        """断开MongoDB连接"""
        if cls.client:
            cls.client.close()
            print("✅ 已断开MongoDB连接")

    @classmethod
    def get_collection(cls, collection_name: str):
        """获取集合"""
        if cls.database is None:
            raise Exception("数据库未连接")
        return cls.database[collection_name]

