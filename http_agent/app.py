import falcon
from http_agent.router import configure_routes
from http_agent.settings import build_settings
from http_agent.utils import make_middlewares
from http_agent.request import Request
from kernel import HelloKernel
import logging
import logging.config
import structlog


# get application settings
settings = build_settings()


# set up logging
logging.config.dictConfig(settings['logging'])
structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())
log = structlog.getLogger(__name__)


# create WSGI app instace
application = falcon.API(
    middleware=make_middlewares(settings),
    request_type=Request
)
application.req_options.keep_blank_qs_values = True
application.req_options.auto_parse_qs_csv = True


# build sub application
core = HelloKernel(**settings['kernel'])
core.initialize_backends()


# add routes
configure_routes(application, core)


# NOTE: don't log secrets from app settings here
log.info("Application ready!", settings=settings)
