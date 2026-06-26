from http import HTTPStatus

from fastapi import Request
from fastapi.responses import JSONResponse
from toolkit.service.response import EmptyData, JSendErrorResponse, JSendFailResponse


class JsendErrorHandler:
    def __init__(self, http_status: HTTPStatus) -> None:
        self._http_status = http_status

    async def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        data: dict | EmptyData = getattr(exc, "data", None) or EmptyData()
        message: str = getattr(exc, "message", None) or self._http_status.phrase

        return JSONResponse(
            status_code=self._http_status,
            content=JSendErrorResponse(message=message, data=data).model_dump(),
        )


class JsendFailHandler:
    def __init__(self, http_status: HTTPStatus) -> None:
        self._http_status = http_status

    async def __call__(self, request: Request, exc: Exception) -> JSONResponse:
        data: dict | EmptyData = getattr(exc, "data", None) or EmptyData()
        message: str = getattr(exc, "message", None) or self._http_status.phrase

        return JSONResponse(
            status_code=self._http_status,
            content=JSendFailResponse(message=message, data=data).model_dump(),
        )
