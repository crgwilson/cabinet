from enum import Enum
from logging import getLogger as get_logger
from typing import Dict, Optional, Tuple

logger = get_logger(__name__)

StatusCode = int
ResponseMessage = str
ResponseBody = Dict[str, ResponseMessage]
Response = Tuple[ResponseBody, StatusCode]


class HTTPStatusCodes(Enum):
    OK: StatusCode = 200
    BAD_REQUEST: StatusCode = 400
    UNAUTHORIZED: StatusCode = 401
    FORBIDDEN: StatusCode = 403
    NOT_FOUND: StatusCode = 404
    INTERNAL_SERVER_ERROR: StatusCode = 500


class HTTPResponseMessages(Enum):
    OK: ResponseMessage = "Success"
    BAD_REQUEST: ResponseMessage = "Bad Request"
    UNAUTHORIZED: ResponseMessage = "Unauthorized"
    FORBIDDEN: ResponseMessage = "Forbidden"
    NOT_FOUND: ResponseMessage = "Not Found"
    INTERNAL_SERVER_ERROR: ResponseMessage = "Internal Server Error"


class CabinetApiResponse(object):
    @classmethod
    def ok(cls) -> Response:
        ok_response = (
            cls._wrap_message(HTTPResponseMessages.OK.value),
            HTTPStatusCodes.OK.value,
        )
        return ok_response

    @classmethod
    def bad_request(cls, message: Optional[str] = None) -> Response:
        if not message:
            message = HTTPResponseMessages.BAD_REQUEST.value

        bad_request_response = (
            cls._wrap_message(message),
            HTTPStatusCodes.BAD_REQUEST.value,
        )

        return bad_request_response

    @classmethod
    def unauthorized(cls) -> Response:
        unauthorized_response = (
            cls._wrap_message(HTTPResponseMessages.UNAUTHORIZED.value),
            HTTPStatusCodes.UNAUTHORIZED.value,
        )

        return unauthorized_response

    @classmethod
    def forbidden(cls) -> Response:
        forbidden_response = (
            cls._wrap_message(HTTPResponseMessages.FORBIDDEN.value),
            HTTPStatusCodes.FORBIDDEN.value,
        )

        return forbidden_response

    @classmethod
    def not_found(cls) -> Response:
        not_found_response = (
            cls._wrap_message(HTTPResponseMessages.NOT_FOUND.value),
            HTTPStatusCodes.NOT_FOUND.value,
        )

        return not_found_response

    @classmethod
    def internal_server_error(cls, message: Optional[str] = None) -> Response:
        if not message:
            message = HTTPResponseMessages.INTERNAL_SERVER_ERROR.value

        internal_server_error_response = (
            cls._wrap_message(message),
            HTTPStatusCodes.INTERNAL_SERVER_ERROR.value,
        )

        return internal_server_error_response

    @staticmethod
    def _wrap_message(msg: str) -> Dict[str, str]:
        return {"message": msg}
