# from __future__ import annotations

# from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, func
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()


# class Item(Base):
#     __tablename__ = "items"

#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), nullable=False)
#     price = Column(Float, nullable=False)
#     in_stock = Column(Boolean, nullable=False, default=True)
#     created_at = Column(
#         DateTime(timezone=True), nullable=False, server_default=func.now()
#     )


from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String, Text
from git_day_practice.db import Base


class RagLog(Base):
    __tablename__ = "rag_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    normalized_query = Column(Text, nullable=False)
    action = Column(String(32), nullable=False)
    reason = Column(Text, nullable=False)
    answer = Column(Text, nullable=False, default="")
    top_score = Column(Float, nullable=False, default=0.0)
    avg_score = Column(Float, nullable=False, default=0.0)
    result_count = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)