"""
PostgreSQL数据库连接
"""
from typing import Optional, Dict, Any, List
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

Base = declarative_base()


class Database:
    """PostgreSQL数据库管理"""

    def __init__(self, url: str):
        self.engine = create_engine(url, pool_size=10, max_overflow=20)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """获取会话"""
        return self.SessionLocal()

    def create_tables(self):
        """创建表"""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """删除表"""
        Base.metadata.drop_all(self.engine)


# 全局实例
_db: Optional[Database] = None


def init_database(url: str) -> Database:
    """初始化数据库"""
    global _db
    _db = Database(url)
    _db.create_tables()
    return _db


def get_database() -> Database:
    """获取数据库实例"""
    if _db is None:
        raise RuntimeError("Database not initialized")
    return _db


# ==================== 通用表模型 ====================


class TaskRecord(Base):
    """任务记录"""
    __tablename__ = "task_records"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(64), unique=True, nullable=False, index=True)
    agent_id = Column(String(64), nullable=False)
    task_type = Column(String(64), nullable=False)
    status = Column(String(32), nullable=False)
    input_data = Column(Text)
    result = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class AgentMemory(Base):
    """Agent记忆持久化"""
    __tablename__ = "agent_memories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(String(64), nullable=False, index=True)
    memory_type = Column(String(32), nullable=False)  # immediate/short_term/long_term/core
    memory_key = Column(String(128))
    content = Column(Text)
    metadata = Column(Text)  # JSON
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
