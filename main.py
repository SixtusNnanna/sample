from datetime import datetime, timedelta

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from schema import UserCreate,TaskCreate, ApplicationCreate, ActivityCreate
from database import Base, get_db, engine
from models import User, Task, Application, Activity


app = FastAPI()


IDLE_THRESHOLD_SECONDS = 10  # Idle time threshold in seconds

Base.metadata.create_all(bind=engine)

@app.get("/root")
async def root():
    return {"message": "Welcome to the FastAPI API!"}

@app.post("/create_user")
def create_user( user_in:UserCreate, db:Session=Depends(get_db)):
    new_user = User(username=user_in.username, email=user_in.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


    
@app.post("/create_task")
def create_task( task_in:TaskCreate, db:Session=Depends(get_db)):
    new_task = Task(project=task_in.project)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.post("/create_application")
def create_application(application_in:ApplicationCreate, db:Session=Depends(get_db)):
    new_application = Application(app_name = application_in.app_ame)
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application


@app.post("/create_activity")
def create_activity(activity_in:ActivityCreate, db:Session=Depends(get_db)):
    new_activity = Activity(**activity_in.dict())
    db.add(new_activity)
    db.commit()
    db.refresh(new_activity)
    return new_activity






# @app.get("/daily/{user_id}")
# async def get_daily_time(user_id: int, db: Session = Depends(get_db)):
#     current_time = datetime.now()
#     start_of_day = current_time.replace(hour=0, minute=0, second=0)
#     end_of_day = current_time.replace(hour=23, minute=59, second=59)

#     user_activities = db.query(Activity).filter(
#         and_(
#             Activity.user_id == user_id,
#             Activity.timestamp >= start_of_day,
#             Activity.timestamp <= end_of_day
#         )
#     ).all()


#     total_time_spent = sum(activity.timestamp  for activity in user_activities)
#     return {
#        "total_time_spent": total_time_spent
#    }


@app.get("/daily/{user_id}")
async def get_daily_time(user_id: int, db: Session = Depends(get_db)):
    current_time = datetime.now()
    start_of_day = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = current_time.replace(hour=23, minute=59, second=59, microsecond=999999)

    user_activities = db.query(Activity).filter(
        and_(
            Activity.user_id == user_id,
            Activity.timestamp >= start_of_day,
            Activity.timestamp <= end_of_day
        )
    ).order_by(Activity.timestamp).all()

    if not user_activities:
        raise HTTPException(status_code=404, detail="No activities found for this user")

    total_time_spent = 0
    previous_activity_timestamp = None

    for activity in user_activities:
        if previous_activity_timestamp is not None:
            # Calculate time spent between this activity and the previous one
            time_spent = (activity.timestamp - previous_activity_timestamp).total_seconds()
            if time_spent < IDLE_THRESHOLD_SECONDS:
                total_time_spent += time_spent
            else:
                total_time_spent += IDLE_THRESHOLD_SECONDS
        previous_activity_timestamp = activity.timestamp

    return {
        "user_id": user_id,
        "total_time_spent_seconds": total_time_spent
    }


@app.get("/weekly/{user_id}")
async def get_weekly_time(user_id: int, db: Session = Depends(get_db)):
    # Get the start and end of the last 7 days
    current_time = datetime.now()
    start_of_week = current_time- timedelta(days=7)
    
    # Fetch activities for the user for the last 7 days
    user_activities = db.query(Activity).filter(
        and_(
            Activity.user_id == user_id,
            Activity.timestamp >= start_of_week,
            Activity.timestamp <= current_time

        )
    )

    if not user_activities:
        raise HTTPException(status_code=404, detail="User not found or no activities for the last 7 days")

    # Calculate the total active time
    total_active_time_seconds = 0
    previous_activity_timestamp = None

    for activity in user_activities:
        if previous_activity_timestamp is not None:
            gap = (activity.timestamp - previous_activity_timestamp).total_seconds()
            if gap < IDLE_THRESHOLD_SECONDS:
                total_active_time_seconds += gap
            else:
                total_active_time_seconds += IDLE_THRESHOLD_SECONDS
        previous_activity_timestamp = activity.timestamp

    return {"user_id": user_id, "total_active_time_seconds": total_active_time_seconds}



@app.get("/monthly/{user_id}")
async def get_monthly_time(user_id: int, db: Session = Depends(get_db)):
    current_time = datetime.now()
    start_of_month = current_time- timedelta(days=30)

    user_activities = db.query(Activity).filter(
        and_(
            Activity.user_id == user_id,
            Activity.timestamp >= start_of_month,
            Activity.timestamp <= current_time
        )
   
    )
    if not user_activities:
        raise HTTPException(status_code=404, detail="User not found or no activities for the last 30 days")
    
    total_active_time_seconds = 0
    previous_activity_timestamp = None

    for activity in user_activities:
        if previous_activity_timestamp is not None:
            gap = (activity.timestamp - previous_activity_timestamp).total_seconds()
            if gap < IDLE_THRESHOLD_SECONDS:
                total_active_time_seconds += gap
            else:
                total_active_time_seconds += IDLE_THRESHOLD_SECONDS
        previous_activity_timestamp = activity.timestamp

    return {"user_id": user_id, "total_active_time_seconds": total_active_time_seconds}




