import logging
import logging.handlers
from logging.handlers import WatchedFileHandler
import os
import multiprocessing

bind = "0.0.0.0:8001"  # 绑定的ip与端口
backlog = 1024  # 监听队列数量，64-2048
worker_class = 'gevent'  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式
workers = 4  # multiprocessing.cpu_count()    #进程数
threads = 8  # multiprocessing.cpu_count()*4 #指定每个进程开启的线程数
timeout = 30
proc_name = 'gunicorn_project'   #进程名
