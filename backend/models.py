from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from database import Base
from datetime import datetime


class Monitor(Base):
    __tablename__ = "monitors"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    interval = Column(Integer, default=30)
    status = Column(String, default="unknown")


class CheckResult(Base):
    __tablename__ = "check_results"

    id = Column(Integer, primary_key=True, autoincrement=True)
    monitor_id = Column(String, ForeignKey("monitors.id"), nullable=False)

    status = Column(String, nullable=False)
    status_code = Column(Integer, nullable=True)
    response_time = Column(Integer, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)
