"""Module: API client."""

from http import HTTPMethod
from typing import Optional, Type, TypeVar

import aiohttp
from pydantic import BaseModel

from .auth_strategies import AbstractAuthorizationStrategy

DTO = TypeVar("DTO", bound=BaseModel)


class APIClient:
    """API Client.

    # TODO: exceptions handling
    # TODO: exceptions logging
    """

    def __init__(
        self, base_url: str, authorization_strategy: Optional[AbstractAuthorizationStrategy] = None
    ) -> None:
        """Initialize client.

        Args:
            base_url (str): Callable service base url.
            authorization_strategy (Optional[AbstractAuthorizationStrategy], optional):
                authorization method to apply. Defaults to None.
        """
        self.base_url = base_url
        self.authorization_strategy = authorization_strategy

    async def __request(
        self,
        method: HTTPMethod,
        endpoint: str,
        headers: Optional[dict] = None,
        payload: Optional[dict] = None,
        data: Optional[dict] = None,
        query: Optional[dict] = None,
    ) -> dict:
        session_headers = {}
        if self.authorization_strategy:
            session_headers.update(**self.authorization_strategy.get_headers())
        if headers:
            session_headers.update(**headers)
        async with aiohttp.ClientSession(self.base_url, headers=session_headers) as _session:
            async with _session.request(
                method, endpoint, params=query, json=payload, data=data
            ) as response:
                return await response.json()

    async def request(
        self,
        method: HTTPMethod,
        endpoint: str,
        headers: Optional[dict] = None,
        payload: Optional[dict] = None,
        data: Optional[dict] = None,
        query: Optional[dict] = None,
    ) -> dict:
        """Make request to the endpoint.

        Args:
            method (HTTPMethod): HTTP method to execute.
            endpoint (str): Endpoint which should be called.
            headers (Optional[dict], optional): Request headers. Defaults to None.
            payload (Optional[dict], optional): Request payload. Defaults to None.
            data (Optional[dict], optional): Request payload. Defaults to None.
            query (Optional[dict], optional): Request query parameters. Defaults to None.

        Returns:
            dict: Response payload data.
        """
        return await self.__request(method, endpoint, headers, payload, data, query)

    async def mapped_request(
        self,
        method: HTTPMethod,
        endpoint: str,
        response_model: Type[DTO],
        headers: Optional[dict] = None,
        payload: Optional[BaseModel] = None,
        query: Optional[BaseModel] = None,
    ) -> DTO:
        """Make request to the endpoint.

        Similar to `.request()` method, but provides request/response validation.

        Args:
            method (HTTPMethod):  HTTP method to execute.
            endpoint (str):  Endpoint which should be called.
            response_model (Type[DTO]): Model by which response should be validated.
            headers (Optional[dict]):  Request headers. Defaults to None.
            payload (Optional[BaseModel]):  Request payload. Defaults to None.
            query (Optional[BaseModel]):  Request query parameters. Defaults to None.

        Returns:
            DTO: Validate response model.
        """
        data = await self.request(
            method,
            endpoint,
            headers,
            payload.model_dump(by_alias=True) if payload else None,
            query.model_dump(by_alias=True) if query else None,
        )
        response_dto = response_model.model_validate(data)

        return response_dto
