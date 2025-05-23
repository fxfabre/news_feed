# Server socket
#   bind - The socket to bind. form: 'HOST', 'HOST:PORT', 'unix:PATH'.
#
#   backlog - The number of pending connections. This refers
#       to the number of clients that can be waiting to be
#       served. Exceeding this number results in the client
#       getting an error when attempting to connect. It should
#       only affect servers under significant load.
#
#       Must be a positive integer. Generally set in the 64-2048 range.
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
#   workers - The number of worker processes that this server
#       should keep alive for handling requests.
#       A positive integer generally in the 2-4 x $(NUM_CORES)
#       range. You'll want to vary this a bit to find the best
#       for your particular application's work load.
# workers = 2 * os.cpu_count() + 1
workers = 1  # not enough ram for more

#   worker_class - The type of workers to use. The default
#       sync class should handle most 'normal' types of work
#       loads. You'll want to read
#       http://docs.gunicorn.org/en/latest/design.html#choosing-a-worker-type
#       for information on when you might want to choose one
#       of the other worker classes.
#
#       A string referring to a Python path to a subclass of
#       gunicorn.workers.base.Worker. The default provided values
#       can be seen at
#       http://docs.gunicorn.org/en/latest/settings.html#worker-class
worker_class = "uvicorn_worker.UvicornWorker"
threads = 1

#   worker_connections - For the eventlet and gevent worker classes
#       this limits the maximum number of simultaneous clients that
#       a single process can handle.
#       A positive integer generally set to around 1000.
# max_requests = 0
worker_connections = 1000

#   timeout - If a worker does not notify the master process in this
#       number of seconds it is killed and a new worker is spawned
#       to replace it.
#       Generally set to thirty seconds. Only set this noticeably
#       higher if you're sure of the repercussions for sync workers.
#       For the non sync workers it just means that the worker
#       process is still communicating and is not tied to the length
#       of time required to handle a single request.
timeout = 900

# graceful_timeout : After receiving a restart signal, workers have
#       this much time to finish serving requests. Workers still alive
#       after the timeout (starting from the receipt of the restart
#       signal) are force killed.
graceful_timeout = 900

#   keepalive - The number of seconds to wait for the next request
#       on a Keep-Alive HTTP connection.
#       A positive integer. Generally set in the 1-5 seconds range.
keepalive = 2

#   spew - Install a trace function that spews every line of Python
#       that is executed when running the server. This is the
#       nuclear option. True or False
spew = False


# region Server mechanics
#
#   daemon - Detach the main Gunicorn process from the controlling
#       terminal with a standard fork/fork sequence.
daemon = False

#   raw_env - Pass environment variables to the execution environment.
# raw_env = [
#     'DJANGO_SECRET_KEY=something',
#     'SPAM=eggs',
# ]

#   pidfile - The path to a pid file to write
#       A path string or None to not write a pid file.
# pidfile = None

#   user - Switch worker processes to run as this user.
#       A valid user id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getpwnam(value) or None
#       to not change the worker process user.
# user = None
#
#   group - Switch worker process to run as this group.
#
#       A valid group id (as an integer) or the name of a user that
#       can be retrieved with a call to pwd.getgrnam(value) or None
#       to change the worker processes group.
# group = None
#
#   umask - A mask for file permissions written by Gunicorn. Note that
#       this affects unix socket permissions.
#
#       A valid value for the os.umask(mode) call or a string
#       compatible with int(value, 0) (0 means Python guesses
#       the base, so values like "0", "0xFF", "0022" are valid
#       for decimal, hex, and octal representations)
# umask = 0
#
#   tmp_upload_dir - A directory to store temporary request data when
#       requests are read. This will most likely be disappearing soon.
#
#       A path to a directory where the process owner can write. Or
#       None to signal that Python should choose one on its own.
# tmp_upload_dir = None
# endregion


# region   Logging
#
#   logfile - The path to a log file to write to.
#       A path string. "-" means log to stdout.
#
#   loglevel - The granularity of log output  (--log-level info)
#       A string of "debug", "info", "warning", "error", "critical"
# errorlog = '-'
loglevel = "info"
# accesslog = '-'
# access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
logconfig = "config/logging.ini"
# endregion


# region Process naming
#
#   proc_name - A base to use with setproctitle to change the way
#       that Gunicorn processes are reported in the system process
#       table. This affects things like 'ps' and 'top'. If you're
#       going to be running more than one instance of Gunicorn you'll
#       probably want to set a name to tell them apart. This requires
#       that you install the setproctitle module.
#
#       A string or None to choose a default of something like 'gunicorn'.
# proc_name = None
# endregion


# region Server hooks
def post_fork(server, worker) -> None:
    """
    post_fork - Called just after a worker has been forked.
        A callable that takes a server and worker instance as arguments.
    """
    server.log.info("Worker spawned (pid: %s)", worker.pid)


def pre_fork(server, worker) -> None:
    """
    pre_fork - Called just prior to forking the worker subprocess.
        A callable that accepts the same arguments as after_fork
    """
    pass


def pre_exec(server) -> None:
    """
    pre_exec - Called just prior to forking off a secondary
        master process during things like config reloading.
        A callable that takes a server instance as the sole argument.
    """
    server.log.info("Forked child, re-executing.")


def when_ready(server) -> None:
    server.log.info("Server is ready. Spawning workers")


def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")


# endregion
