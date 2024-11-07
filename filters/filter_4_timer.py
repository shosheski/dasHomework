import time

def start_timer():
    return time.time()

def stop_timer(start_time):
    end_time = time.time()
    return end_time - start_time

def log_time(elapsed_time, log_file_path="execution_time.txt"):
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((elapsed_time % 1) * 1000)
    with open(log_file_path, "w") as f:
        f.write(f"{int(hours)}:{int(minutes)}:{int(seconds)}:{milliseconds}\n")