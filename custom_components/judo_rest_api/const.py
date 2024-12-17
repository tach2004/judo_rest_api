"""Constants."""

from dataclasses import dataclass
from datetime import timedelta

from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_PASSWORD,
    CONF_USERNAME,
)


@dataclass(frozen=True)
class ConfConstants:
    """Constants used for configurastion"""

    HOST = CONF_HOST
    PORT = CONF_PORT
    PASSWORD = CONF_PASSWORD
    USERNAME = CONF_USERNAME
    DEVICE_POSTFIX = "Device-Postfix"


CONF = ConfConstants()


@dataclass(frozen=True)
class MainConstants:
    """Main constants."""

    DOMAIN = "judo_rest_api"
    SCAN_INTERVAL = timedelta(seconds=30)
    UNIQUE_ID = "unique_id"
    APPID = 100


CONST = MainConstants()


@dataclass(frozen=True)
class FormatConstants:
    """Format constants."""

    NUMBER = "number"
    TEXT = "text"
    STATUS = "status"
    UNKNOWN = "unknown"


FORMATS = FormatConstants()


@dataclass(frozen=True)
class TypeConstants:
    """Type constants."""

    SENSOR = "Sensor"
    SENSOR_CALC = "Sensor_Calc"
    SELECT = "Select"
    NUMBER = "Number"
    NUMBER_RO = "Number_RO"


TYPES = TypeConstants()


@dataclass(frozen=True)
class DeviceConstants:
    """Device constants."""

    SYS = "dev_system"
    ST = "dev_statistics"
    UK = "dev_unknown"


DEVICES = DeviceConstants()

COMMANDS = {
    "Geraetetyp": "FF00",
    "Geraetenummer": "0600",
    "SW-Version": "0100",
    "Inbetriebnahmedatum": "0E00",
    "Betriebsstundenzaehler": "2500",
    "Kundendienst-Serviceadresse": "5800",
    "Wunschwasserhaerte": "5100",
    "Salzvorrat": "5600",
    "Salzreichweite": "5700",
    "Gesamtwassermenge": "2800",
    "Weichwassermenge": "2900",
    "Tagesstatistik": "FB00",
    "Wochenstatistik": "FC00",
    "Monatsstatistik": "FD00",
    "Jahresstatistik": "FE00",
}


DEVICETYPES = {
    "33": "i-soft SAFE+",
    "42": "i-soft K SAFE+",
    "58": "i-soft PRO",
    "4B": "i-soft PRO",
    "4C": "i-soft PRO L",
    "32": "i-soft",
    "43": "i-soft K",
    "34": "SOFTwell P",
    "35": "SOFTwell S",
    "36": "SOFTwell K",
    "47": "SOFTwell KP",
    "72": "SOFTwell KS",
    "44": "ZEWA/PROM i-SAFE (FILT)",
    "41": "i-dos eco",
    "3c": "i-fill",
}
