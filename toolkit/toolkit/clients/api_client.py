from typing import Optional, TypeVar, Type
import aiohttp
from http import HTTPMethod
from pydantic import BaseModel
from .auth_strategies import AbstractAuthorizationStrategy


DTO = TypeVar("DTO", bound=BaseModel)


class APIClient:

    def __init__(self, base_url: str, authorization_strategy: Optional[AbstractAuthorizationStrategy] = None) -> None:
        self.base_url = base_url
        self.authorization_strategy = authorization_strategy

    async def __request(
        self,
        method: HTTPMethod,
        endpoint: str,
        headers: Optional[dict] = None,
        payload: Optional[dict] = None,
        query: Optional[dict] = None,
    ) -> dict:
        session_headers = {}
        if self.authorization_strategy:
            session_headers.update(**self.authorization_strategy.get_headers())
        if headers:
            session_headers.update(**headers)
        async with aiohttp.ClientSession(self.base_url, headers=session_headers) as _session:
            async with _session.request(method, endpoint, params=query, json=payload) as response:
                return await response.json()


    async def request(
        self,
        method: HTTPMethod,
        endpoint: str,
        headers: Optional[dict] = None,
        payload: Optional[dict] = None,
        query: Optional[dict] = None,
    ) -> dict:
        return await self.__request(method, endpoint, headers, payload, query)

    async def mapped_request(
        self,
        method: HTTPMethod,
        endpoint: str,
        response_model: Type[DTO],
        headers: Optional[dict] = None,
        payload: Optional[BaseModel] = None,
        query: Optional[BaseModel] = None,
    ) -> DTO:
        data = await self.request(
            method,
            endpoint,
            headers,
            payload.model_dump(by_alias=True) if payload else None,
            query.model_dump(by_alias=True) if query else None
        )
        response_dto = response_model.model_validate(data)

        return response_dto
