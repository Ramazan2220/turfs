import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class TaskStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class InstagramAccount(Base):
    __tablename__ = 'instagram_accounts'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    proxy_id = Column(Integer, ForeignKey('proxies.id'), nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    # Новые поля для работы с сессиями и email
    email = Column(String(255), nullable=True)
    email_password = Column(String(255), nullable=True)
    session_data = Column(Text, nullable=True)  # Для хранения данных сессии в JSON
    last_login = Column(DateTime, nullable=True)  # Время последнего успешного входа

    # Отношения
    proxy = relationship("Proxy", back_populates="accounts")
    tasks = relationship("PublishTask", back_populates="account")

class Proxy(Base):
    __tablename__ = 'proxies'

    id = Column(Integer, primary_key=True)
    proxy_type = Column(String(50), nullable=False)  # http, https, socks4, socks5
    host = Column(String(255), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Отношения
    accounts = relationship("InstagramAccount", back_populates="proxy")

class PublishTask(Base):
    __tablename__ = 'publish_tasks'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey('instagram_accounts.id'), nullable=False)
    task_type = Column(String(50), nullable=False)  # video, photo, carousel
    media_path = Column(String(255), nullable=False)
    caption = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    error_message = Column(Text, nullable=True)
    media_id = Column(String(255), nullable=True)
    scheduled_time = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    completed_at = Column(DateTime, nullable=True)

    # Отношения
    account = relationship("InstagramAccount", back_populates="tasks")
