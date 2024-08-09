import datetime as dt
from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int


class TaskBase(BaseModel):
    project: str


class TaskCreate(TaskBase):
    pass 


class Task(TaskBase):
    id: int


class ApplicationBase(BaseModel):
    app_ame: str


class ApplicationCreate(ApplicationBase):
    pass


class Application(ApplicationBase):
    id: int



class ActivityBase(BaseModel):
    activity_type: str



class ActivityCreate(ActivityBase):
    user_id: int
    task_id: int
    application_id: int


class Activity(ActivityBase):
    id: int
    timestamp: datetime
    user_id: int
    task_id: int
    application_id: int


