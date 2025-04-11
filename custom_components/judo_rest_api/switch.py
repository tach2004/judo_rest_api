"""Setting up my sensor entities."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .configentry import MyConfigEntry
from .const import TYPES
from .entity_helpers import build_entity_list
from .jdconst import DEVICELISTS

logging.basicConfig()
log: logging.Logger = logging.getLogger(name=__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""

    _useless = hass
    # start with an empty list of entries
    entries = []

    # we create one communicator per integration only for better performance and to allow dynamic parameters
    coordinator = config_entry.runtime_data.coordinator

    for device in DEVICELISTS:
        entries = await build_entity_list(
            entries=entries,
            config_entry=config_entry,
            rest_items=device,
            item_type=TYPES.SWITCH,
            coordinator=coordinator,
        )

    async_add_entities(
        entries,
        update_before_add=True,
    )
