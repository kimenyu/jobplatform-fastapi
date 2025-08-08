import multiprocessing

bind = "0.0.0.0:8000"
workers = max(2, multiprocessing.cpu_count() * 2 + 1)  # pre-fork
worker_class = "uvicorn.workers.UvicornWorker"
accesslog = "-"
errorlog = "-"
loglevel = "info"
timeout = 60
