from __future__ import annotations

import asyncio
import ssl
from typing import Any, TYPE_CHECKING

from aiohttp import ClientError, ClientSession, FormData, TCPConnector
from ujson import dumps, loads

from qa_bot import utils

if TYPE_CHECKING:
    from collections.abc import Mapping

    from yarl import URL


# Taken from here: https://github.com/Olegt0rr/WebServiceTemplate/blob/main/app/core/base_client.py
class BaseClient:
    """Represents base API client."""

    def __init__(self, base_url: str | URL, api_key: str | None = None) -> None:
        self._base_url = base_url
        self._api_key = api_key
        self._session: ClientSession | None = None
        self._accept_statuses = [200, 201, 400, 409]
        self.log = utils.logging.setup_logger().bind(type="aiogram_session")

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None:
            ssl_context = ssl.SSLContext()
            connector = TCPConnector(ssl_context=ssl_context)
            self._session = ClientSession(
                base_url=self._base_url,
                connector=connector,
                json_serialize=dumps,
            )

        return self._session

    def _add_api_key(
        self, headers: Mapping[str, str] | None = None
    ) -> Mapping[str, str]:
        if headers is None:
            headers = {}
        headers["Authorization"] = f"Token {self._api_key}"
        return headers

    async def _make_authenticated_request(
        self,
        method: str,
        url: str | URL,
        params: Mapping[str, str] | None = None,
        json: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        data: FormData | None = None,
    ) -> tuple[int, dict[str, Any]]:
        """Make authenticated request with API key."""
        authenticated_headers = self._add_api_key(headers)
        return await self._make_request(
            method, url, params, json, authenticated_headers, data
        )

    async def _make_request(
        self,
        method: str,
        url: str | URL,
        params: Mapping[str, str] | None = None,
        json: Mapping[str, str] | None = None,
        headers: Mapping[str, str] | None = None,
        data: FormData | None = None,
    ) -> tuple[int, dict[str, Any]]:
        """Make request and return decoded json response."""
        session = await self._get_session()

        self.log.debug(
            "Making request %r %r with json %r and params %r",
            method,
            url,
            json,
            params,
        )
        async with session.request(
            method, url, params=params, json=json, headers=headers, data=data
        ) as response:
            status = response.status
            if status not in self._accept_statuses:
                s = await response.text()
                raise ClientError(f"Got status {status} for {method} {url}: {s}")
            try:
                result = await response.json(loads=loads)
            except Exception as e:
                self.log.exception(e)
                self.log.info(f"{await response.text()}")
                result = {}

        self.log.debug(
            "Got response %r %r with status %r and json %r",
            method,
            url,
            status,
            result,
        )
        return status, result

    async def close(self) -> None:
        """Graceful session close."""
        if not self._session:
            self.log.debug("There's not session to close.")
            return

        if self._session.closed:
            self.log.debug("Session already closed.")
            return

        await self._session.close()
        self.log.debug("Session successfully closed.")

        # Wait 250 ms for the underlying SSL connections to close
        # https://docs.aiohttp.org/en/stable/client_advanced.html#graceful-shutdown
        await asyncio.sleep(0.25)
