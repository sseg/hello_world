bind = "127.0.0.1:9090"
workers = 1
max_requests = 1_000
max_request_jitter = max_requests / 10
timeout = 2
accesslog = '-'
access_log_format = (
    "ip='%(h)s' request='%(r)s' response_status=%(s)s "
    "resp_size_bytes=%(b)s elapsed_us=%(D)s request_id='%({Request-Id}o)s' "
    "referrer='%({Referrer}i)s' user_agent='%({User-Agent}i)s'"
)
