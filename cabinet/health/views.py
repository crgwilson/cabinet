from logging import getLogger as get_logger

from flask import Blueprint

from flask_restful import Api

from cabinet.api import CabinetResource
from cabinet.response import CabinetApiResponse
from cabinet._types import ApiResponse

logger = get_logger(__name__)

bp = Blueprint("health", __name__)
api = Api(bp)


class HealthCheck(CabinetResource):
    def get(self) -> ApiResponse:
        return CabinetApiResponse.ok()


api.add_resource(HealthCheck, "/health", endpoint="health")
