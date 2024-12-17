"""Heatpump constants."""

from homeassistant.components.sensor import SensorDeviceClass, SensorStateClass
from homeassistant.const import (
    UnitOfEnergy,
    UnitOfVolumeFlowRate,
)

from .const import DEVICES, FORMATS, TYPES
from .items import RestItem, StatusItem

reverse_device_list: dict[str, str] = {
    "dev_system": "SYS",
    "dev_statistik": "ST",
}

################################################################################
# Listen mit Fehlermeldungen, Warnmeldungen und Statustexte
# Beschreibungstext ist ebenfalls möglich
# class StatusItem(): def __init__(self, number, text, description = None):
################################################################################

# fmt: off

UNIT_STATUS: list[StatusItem] = [
    StatusItem(number=0, translation_key="ge_hardness"),
    StatusItem(number=1, translation_key="en_hardness"),
    StatusItem(number=2, translation_key="fr_hardness"),
    StatusItem(number=3, translation_key="ppm"),
    StatusItem(number=4, translation_key="mmol"),
    StatusItem(number=5, translation_key="mval"),
]

UNIT_TYPE: list[StatusItem] = [
    StatusItem(number=0x33, translation_key= "i_soft_safe_plus"),
    StatusItem(number=0x42, translation_key=  "i_soft_k_safe_plus"),
    StatusItem(number=0x58, translation_key=  "i_soft_pro"),
    StatusItem(number=0x4B, translation_key=  "i_soft_pro"),
    StatusItem(number=0x4C, translation_key=  "i_soft_pro_l"),
    StatusItem(number=0x32, translation_key=  "i_soft"),
    StatusItem(number=0x43, translation_key=  "i_soft_k"),
    StatusItem(number=0x34, translation_key=  "softwell_p"),
    StatusItem(number=0x35, translation_key=  "softwell_s"),
    StatusItem(number=0x36, translation_key=  "softwell_k"),
    StatusItem(number=0x47, translation_key=  "softwell_kp"),
    StatusItem(number=0x72, translation_key=  "softwell_ks"),
    StatusItem(number=0x44, translation_key=  "zewa_prom_i_safe"),
    StatusItem(number=0x41, translation_key=  "i_dos_eco"),
    StatusItem(number=0x3c, translation_key=  "i_fill"),
]

#####################################################
# Description of physical units via the status list #
#####################################################

PARAMS_FLOWRATE: dict = {
    "min": 0,
    "max": 5,
    "step": 0.1,
    "divider": 100,
    "precision": 2,
    "unit": UnitOfVolumeFlowRate.CUBIC_METERS_PER_HOUR,
    "stateclass": SensorStateClass.MEASUREMENT,
}

PARAMS_WATER: dict = {
    "min": 0,
    "max": 999999999999,
    "deviceclass": SensorDeviceClass.ENERGY,
    "precision": 0,
    "unit": UnitOfEnergy.KILO_WATT_HOUR,
    "stateclass": SensorStateClass.TOTAL_INCREASING,
}



# pylint: disable=line-too-long

# fmt: off
REST_SYS_ITEMS: list[RestItem] = [
    RestItem( address_read="FF00", read_bytes = 2, read_index=0, mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.SYS, resultlist=UNIT_TYPE, translation_key="device_type"),
    RestItem( address_read="0600", read_bytes = 4, read_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, translation_key="device_number"),
    RestItem( address_read="0100", read_bytes = 3, read_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, translation_key="software_version"),
    RestItem( address_read="5100", read_bytes = 2, read_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, translation_key="water_hardeness"),
    RestItem( address_read="5600", read_bytes = 2, read_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, translation_key="salt_storage_mass"),
    RestItem( address_read="5600", read_bytes = 2, read_index=2, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, translation_key="salt_storage_days"),
]

REST_ST_ITEMS: list[RestItem] = [
    RestItem( address_read="FB00", mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.ST, params=PARAMS_WATER, translation_key="day_statistics"),
]

DEVICELISTS: list = [
    REST_SYS_ITEMS,
    REST_ST_ITEMS,
]

# fmt: on
