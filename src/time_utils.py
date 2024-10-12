import random
from datetime import datetime, timedelta
import time
import logging
import os

# Ensure the log directory exists
log_directory = 'log'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Set up logging to a file in the log directory
logging.basicConfig(
    filename=os.path.join(log_directory, 'general.log'), 
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def calculate_refresh_interval():
    # Calculate a random refresh interval between 30 minutes to 3 hours
    refresh_interval = random.randint(1800, 10800)
    logging.debug("Calculated refresh interval: %d seconds", refresh_interval)
    return refresh_interval

def calculate_next_refresh(current_time, refresh_interval):
    # Calculate the next refresh time based on the current time and refresh interval
    next_refresh = current_time + timedelta(seconds=refresh_interval)
    logging.debug("Calculated next refresh time: %s", next_refresh)
    return next_refresh

def format_time_remaining(time_remaining):
    hours = int(time_remaining.total_seconds()) // 3600
    minutes = int((time_remaining.total_seconds() % 3600) // 60)
    seconds = int(time_remaining.total_seconds() % 60)
    formatted_time = f"{hours} hour{'s' if hours != 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''}, {seconds} second{'s' if seconds != 1 else ''}"
    logging.debug("Formatted time remaining: %s", formatted_time)
    return formatted_time

def sleep_until_next_refresh(next_refresh):
    current_time = datetime.now()
    time_remaining = next_refresh - current_time

    if time_remaining.total_seconds() > 0:
        print(f"Time until next post refresh: {format_time_remaining(time_remaining)}")
        logging.info("Sleeping for %d seconds until next refresh.", time_remaining.total_seconds())
        time.sleep(time_remaining.total_seconds())
    else:
        logging.warning("Next refresh time is in the past. No sleep required.")