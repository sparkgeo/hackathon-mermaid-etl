import os

num_avail_cpus = len(os.sched_getaffinity(0))

loglevel = os.environ.get("LOG_LEVEL", "INFO")
worker_class = "uvicorn.workers.UvicornWorker"
workers = 2  # 2 * num_avail_cpus    # debugging too many connections issue
bind = "0.0.0.0:8080"
