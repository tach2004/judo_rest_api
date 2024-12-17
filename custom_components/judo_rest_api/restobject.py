"""RESTobject.

A REST object that contains a REST item and communicates with the REST-API.
It contains a REST Client for setting and getting REST response values
"""

import logging
from functools import partial
import requests
from homeassistant.core import HomeAssistant

from .configentry import MyConfigEntry
from .const import DEVICETYPES, FORMATS, CONF
from .items import RestItem

logging.basicConfig()
log = logging.getLogger(__name__)


class RestAPI:
    """
    RestAPI class that provides a connection to the rest api,
    which is used by the RestItems.
    """

    def __init__(self, config_entry: MyConfigEntry, hass: HomeAssistant) -> None:
        """Construct RestAPI.

        :param config_entry: HASS config entry
        :type config_entry: MyConfigEntry
        """
        self._ip = config_entry.data[CONF.HOST]
        self._port = config_entry.data[CONF.PORT]
        self._username = config_entry.data[CONF.USERNAME]
        self._password = config_entry.data[CONF.PASSWORD]
        self._hass = hass
        self._rest_client = None
        self._base_url = (
            "http://"
            # + str(self._user)
            # + ":"
            # + str(self._password)
            # + "@"
            + str(self._ip)
            + ":"
            + str(self._port)
        )
        self._api_url = self._base_url + "/api/rest/"
        self._devicetype = None
        self._session = None
        self._connected = False

    async def login(self) -> None:
        """Log into the portal. Create cookie to stay logged in for the session."""

        r = await self._hass.async_add_executor_job(
            partial(
                requests.get,
                url=self._base_url,
                auth=(self._username, self._password),
                timeout=10,
            )
        )

        # r = requests.get(self._base_url, auth=(self._username, self._password), timeout=10 )
        # log.warning(r.text)

    async def get_rest(self, command: str):
        """get raw response from REST api"""
        try:
            url = self._api_url + command
            response = await self._hass.async_add_executor_job(
                partial(
                    requests.get,
                    url=url,
                    auth=(self._username, self._password),
                    timeout=10,
                )
            )
            res = response.json()
            return res["data"]
        except Exception:
            log.warning("Connection to Judo Water Treatment failed")
            return None

    async def connect(self):
        """Open REST connection to test if available."""
        res = await self.get_rest("FF00")
        if res is None:
            return None
        if res in DEVICETYPES:
            self._devicetype = res
            log.info("Connected to %s", self._devicetype)
            return True

        log.warning("Unknown Device detected, ID=%s", res)
        return None

    def close(self):
        """Close REST connection."""
        log.info("Connection to judo closed")
        return True

    def get_devicetype(self):
        """Return device type."""
        return self._devicetype


class RestObject:
    """RestObject.

    A REST object that contains a REST item and communicates with the REST.
    It contains a REST Client for setting and getting REST register values
    """

    def __init__(self, rest_api: RestAPI, rest_item: RestItem) -> None:
        """Construct RestObject.

        :param rest_api: The REST API
        :type rest_api: RestAPI
        :param rest_item: definition of rest item
        :type rest_item: RestItem
        """
        self._rest_item = rest_item
        self._rest_api = rest_api

    def get_val(self, text: str, byte: int, byte_len: int) -> int:
        index = byte * 2
        big_endian = text[index : index + byte_len * 2]
        little_endian = bytes.fromhex(big_endian)[::-1].hex()
        return int(little_endian, 16)

    def get_status(self, text: str, byte: int, byte_len: int) -> str:
        index = byte * 2
        big_endian = text[index : index + byte_len * 2]
        little_endian = bytes.fromhex(big_endian)[::-1].hex()
        return self._rest_item.get_translation_key_from_number(int(little_endian, 16))

    def get_text(self, text: str, byte: int, byte_len: int) -> str:
        index = byte * 2
        big_endian = text[index : index + byte_len * 2]
        return bytearray.fromhex(big_endian).decode()

    @property
    async def value(self):
        """Returns the value from the REST API."""
        if self._rest_api is None:
            return None

        res = await self._rest_api.get_rest(self._rest_item.address_read)
        match self._rest_item.format:
            case FORMATS.NUMBER:
                return self.get_val(
                    res, self._rest_item.read_index, self._rest_item.read_bytes
                )
            case FORMATS.TEXT:
                return self.get_text(
                    res, self._rest_item.read_index, self._rest_item.read_bytes
                )
            case FORMATS.STATUS:
                return self.get_status(
                    res, self._rest_item.read_index, self._rest_item.read_bytes
                )
            case _:
                log.warning(
                    "Unknown format: %s in %s",
                    str(self._rest_item.type),
                    str(self._rest_item.translation_key),
                )
                return None
        return None

    # @value.setter
    async def setvalue(self, value) -> None:
        """Set the value of the rest register, does nothing when not R/W.

        :param val: The value to write to the rest
        :type val: int"""
        if self._rest_api is None:
            return
        return None
