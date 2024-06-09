import random
from datetime import datetime, timedelta
import time

def calculate_refresh_interval():
    # Calculate a random refresh interval between 30 minutes to 3 hours
    return random.randint(1800, 10800)

def calculate_next_refresh(current_time, refresh_interval):
    # Calculate the next refresh time based on the current time and refresh interval
    return current_time + timedelta(seconds=refresh_interval)

def format_time_remaining(time_remaining):
    hours = int(time_remaining.total_seconds()) // 3600
    minutes = int((time_remaining.total_seconds() % 3600) // 60)
    seconds = int(time_remaining.total_seconds() % 60)
    return f"{hours} hour{'s' if hours != 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''}, {seconds} second{'s' if seconds != 1 else ''}"

def sleep_until_next_refresh(next_refresh):
    current_time = datetime.now()
    time_remaining = next_refresh - current_time

    if time_remaining.total_seconds() > 0:
        print(f"Time until next post refresh: {format_time_remaining(time_remaining)}")
        time.sleep(time_remaining.total_seconds())
