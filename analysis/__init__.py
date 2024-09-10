import time

def exponential_backoff(attempts: int):
    max_sleep_time = 60  # Maximum sleep time capped at 60 seconds
    sleep_time = min(2 ** attempts, max_sleep_time)
    time.sleep(sleep_time)