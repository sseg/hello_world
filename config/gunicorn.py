from dotenv import load_dotenv
from os.path import join, dirname
import os
import gunicorn


gunicorn.SERVER_SOFTWARE = 'An HTTP-compliant server'

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

bind = "%s:%s" % (os.environ['GUNICORN_ADDRESS'], os.environ['GUNICORN_PORT'])
workers = int(os.environ['GUNICORN_WORKERS'])
timeout = int(os.environ['GUNICORN_TIMEOUT'])
graceful_timeout = timeout
max_requests = 10_000
max_request_jitter = max_requests / 10
accesslog = '-'
access_log_format = (
    "ip='%(h)s' request='%(r)s' response_status=%(s)s "
    "resp_size_bytes=%(b)s elapsed_us=%(D)s request_id='%({Request-Id}o)s' "
    "referrer='%({Referrer}i)s' user_agent='%({User-Agent}i)s'"
)
