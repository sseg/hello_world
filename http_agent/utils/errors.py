import falcon
from kernel.errors import (
    AppError,
    ValidationError,
    DataNotFound
)
import structlog


log = structlog.getLogger(__name__)


def kernel_error_handler(view):  # noqa: C901
    def inner(self, req, resp, *args, **kwargs):
        try:
            return view(self, req, resp, *args, **kwargs)
        except AppError as err:
            log.warn("Application error caught", exc_info=True, request_id=req.id)

            if isinstance(err, ValidationError):
                raise falcon.HTTPBadRequest(description=str(err.__cause__)) from err

            if isinstance(err, DataNotFound):
                raise falcon.HTTPNotFound from err

            # unexpected Kernel error
            raise err
    return inner
