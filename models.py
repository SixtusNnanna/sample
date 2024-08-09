import datetime as dt

from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String,  index=True)
    email = Column(String, index=True)
    activities = relationship("Activity", back_populates="user")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    project = Column(String, index=True)
    activities = relationship("Activity", back_populates="task")


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    app_name = Column(String,  index=True)
    activities = relationship("Activity", back_populates="applications")

    


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(String, nullable=False)
    application_id = Column(Integer, ForeignKey("applications.id"))
    timestamp = Column(DateTime, default=datetime.now(dt.UTC))

    # relationships
    user = relationship("User", back_populates="activities")
    task = relationship("Task", back_populates="activities")
    applications = relationship("Application", back_populates="activities")

