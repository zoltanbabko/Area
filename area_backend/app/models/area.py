from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey
from app.database import Base


class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    action = Column(String, nullable=False)
    reaction = Column(String, nullable=False)
    action_params = Column(JSON, nullable=False, default={})
    reaction_params = Column(JSON, nullable=False, default={})
    is_active = Column(Boolean, nullable=False, default=True)
