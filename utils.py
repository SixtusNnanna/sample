@time_router.get("/daily/{user_id}")
async def get_daily_time(user_id: int, db: Session = Depends(sql_factory.get_db)):
    # Get the start and end of the current day
    today = datetime.now()
    today_start = datetime.combine(today, datetime.min.time())
    today_end = datetime.combine(today, datetime.max.time())
    # Fetch activities for the user for today
    user_activities = sql_factory.get_object_list(
        db,
        model=Activity,
        user_id=user_id,
        timestamp=(Activity.timestamp >= today_start, Activity.timestamp <= today_end)
    )
    if not user_activities:
        raise HTTPException(status_code=404, detail="User not found or no activities for today")
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