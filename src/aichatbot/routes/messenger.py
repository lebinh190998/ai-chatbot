import os

import requests
from fastapi import APIRouter, FastAPI, HTTPException, Query, Depends
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_402_PAYMENT_REQUIRED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_423_LOCKED,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_408_REQUEST_TIMEOUT,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from datetime import datetime

from ..config import config
from .. import logger
from ..utils.utils import (
    convert_str_to_iso_datetime,
    success_response,
    failure_response,
    failure_response_kit_registration,
    get_current_date_time,
    convert_datetime_to_iso,
    validate_email
)

router = APIRouter()

@router.get("/kit_results", status_code=HTTP_200_OK)
async def get_results_info(
) -> list:
    """
    Get information of all kit_results
    :return: Kit results information
    """
    logger.info(f"Get kit results info")
    
    return True

def init_app(app: FastAPI):
    app.include_router(router, tags=["aichatbot_messenger"])