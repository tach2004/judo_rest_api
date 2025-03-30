"""Entity classes used in this integration"""

import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.components.number import NumberEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.components.select import SelectEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .configentry import MyConfigEntry
from .const import CONF, CONST, FORMATS
from .coordinator import MyCoordinator
from .items import RestItem
from .restobject import RestAPI, RestObject

from .storage import save_last_written_value, load_last_written_values, PERSISTENT_ENTITIES

logging.basicConfig()
log = logging.getLogger(__name__)


class MyEntity(Entity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
    should_poll
    async_update
    async_added_to_hass
    available

    The base class for entities that hold general parameters
    """

    _attr_should_poll = True
    _attr_has_entity_name = True
    _attr_entity_name = None
    _divider = 1

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        rest_api: RestAPI,
    ) -> None:
        """Initialize the entity."""
        self._config_entry = config_entry
        self._rest_item = rest_item
        self._rest_api = rest_api

        dev_postfix = "_" + self._config_entry.data[CONF.DEVICE_POSTFIX]

        if dev_postfix == "_":
            dev_postfix = ""

        self._dev_device = self._rest_item.device + dev_postfix

        self._attr_translation_key = self._rest_item.translation_key
        self._dev_translation_placeholders = {"postfix": dev_postfix}

        dev_postfix = "_" + config_entry.data[CONF.DEVICE_POSTFIX]
        if dev_postfix == "_":
            dev_postfix = ""

        # self._dev_device = self._rest_api.get_devicetype()
        self._dev_device = self._rest_item.device

        self._attr_unique_id = (
            CONST.DOMAIN
            + "_"
            + self._dev_device
            + "_"
            + self._rest_item.translation_key
        )

        self._rest_api = rest_api

        match self._rest_item.format:
            case FORMATS.STATUS |FORMATS.STATUS_WO | FORMATS.TEXT | FORMATS.TIMESTAMP | FORMATS.SW_VERSION:
                self._divider = 1
            case _:
                # default state class to record all entities by default
                self._attr_state_class = SensorStateClass.MEASUREMENT
                if self._rest_item.params is not None:
                    self._attr_state_class = self._rest_item.params.get(
                        "stateclass", SensorStateClass.MEASUREMENT
                    )
                    self._attr_native_unit_of_measurement = self._rest_item.params.get(
                        "unit", ""
                    )
                    self._attr_native_step = self._rest_item.params.get("step", 1)
                    self._divider = self._rest_item.params.get("divider", 1)
                    self._attr_device_class = self._rest_item.params.get(
                        "deviceclass", None
                    )
                    self._attr_suggested_display_precision = self._rest_item.params.get(
                        "precision", 2
                    )
                    self._attr_native_min_value = self._rest_item.params.get(
                        "min", -999999
                    )
                    self._attr_native_max_value = self._rest_item.params.get(
                        "max", 999999
                    )

        if self._rest_item.params is not None:
            icon = self._rest_item.params.get("icon", None)
            if icon is not None:
                self._attr_icon = icon

    def my_device_info(self) -> DeviceInfo:
        """Build the device info."""
        return {
            "identifiers": {(CONST.DOMAIN, self._dev_device)},
            "translation_key": self._dev_device,
            "translation_placeholders": self._dev_translation_placeholders,
            "sw_version": "Device_SW_Version",
            "model": "Device_model",
            "manufacturer": "Judo",
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MySensorEntity.my_device_info(self)


class MySensorEntity(CoordinatorEntity, SensorEntity, MyEntity):
    """Class that represents a sensor entity.

    Derived from Sensorentity
    and decorated with general parameters from MyEntity
    """

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialize of MySensorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx
        MyEntity.__init__(self, config_entry, rest_item, coordinator.rest_api)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self._rest_item.state
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)


class MyNumberEntity(CoordinatorEntity, NumberEntity, MyEntity):  # pylint: disable=W0223
    """Represent a Number Entity.

    Class that represents a number entity derived from NumberEntity
    and decorated with general parameters from MyEntity
    """

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialize NyNumberEntity."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        self._coordinator = coordinator
        MyEntity.__init__(self, config_entry, rest_item, coordinator.rest_api)
        
        self._attr_mode = "box"  # Setzt die Eingabebox statt des Sliders

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self._rest_item.state
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Send value over modbus and refresh HA."""
        # Ensure we are dealing with the correct translation keys
        ro = RestObject(self._rest_api, self._rest_item)
        await ro.setvalue(value)  # rest_item.state will be set inside ro.setvalue
        self._attr_native_value = self._rest_item.state
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)


class MySwitchEntity(CoordinatorEntity, SwitchEntity, MyEntity):  # pylint: disable=W0223
    """Represent a Number Entity.

    Class that represents a number entity derived from NumberEntity
    and decorated with general parameters from MyEntity
    """

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialize NyNumberEntity."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, rest_item, coordinator.rest_api)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self._rest_item.state
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        ro = RestObject(self._rest_api, self._rest_item)
        await ro.setvalue(1)  # rest_item.state will be set inside ro.setvalue
        self._attr_is_on = self._rest_item.state
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        ro = RestObject(self._rest_api, self._rest_item)
        await ro.setvalue(0)  # rest_item.state will be set inside ro.setvalue
        self._attr_is_on = self._rest_item.state
        self.async_write_ha_state()

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)


class MyButtonEntity(CoordinatorEntity, ButtonEntity, MyEntity):  # pylint: disable=W0223
    """Represent a Number Entity.

    Class that represents a number entity derived from NumberEntity
    and decorated with general parameters from MyEntity
    """

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialize NyNumberEntity."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, rest_item, coordinator.rest_api)

    async def async_press(self):
        """Turn the entity on."""
        ro = RestObject(self._rest_api, self._rest_item)
        await ro.setvalue()  # rest_item.state will be set inside ro.setvalue

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)


class MySelectEntity(CoordinatorEntity, SelectEntity, MyEntity):  # pylint: disable=W0223
    """Class that represents a sensor entity.
    Class that represents a sensor entity derived from Sensorentity
    and decorated with general parameters from MyEntity
    """
    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialize MySelectEntity."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, rest_item, coordinator.rest_api)
        # option list build from the status list of the ModbusItem
        self.options = []
        for _useless, item in enumerate(self._rest_item.resultlist):
            self.options.append(item.translation_key)
        self._attr_current_option = "FEHLER"

    async def async_added_to_hass(self) -> None:
        """When entity is added to hass."""
        await super().async_added_to_hass()
        
        if self._rest_item.translation_key in PERSISTENT_ENTITIES:
            stored_values = await load_last_written_values(self.hass)
            if self._rest_item.translation_key in stored_values:
                self._attr_current_option = stored_values[self._rest_item.translation_key]
                self._rest_item.state = stored_values[self._rest_item.translation_key]
                log.debug("Geladene Werte nach If: %s", stored_values)

    async def async_select_option(self, option: str) -> None:
        """Aktualisiert die Auswahl der Entität und synchronisiert sie mit Home Assistant."""

        #1 special mode absence limit
        if self._rest_item.translation_key in ["absence_limit_max_waterflowrate", "absence_limit_max_water_flow", "absence_limit_max_waterflow_time"]:
            if not self.coordinator._restitems:
                raise ValueError("coordinator._restitems ist None oder leer. Keine Entitäten zum Verarbeiten.")

            selected_values = {}

            for item in self.coordinator._restitems:
                if item.translation_key in ["absence_limit_max_waterflowrate", "absence_limit_max_water_flow", "absence_limit_max_waterflow_time"]:
                    if item.translation_key == self._rest_item.translation_key:
                        # Falls es die aktuelle Entität ist, nehmen wir den neuen Wert (option)
                        selected_value = next(
                            (entry.number for entry in item.resultlist if entry.translation_key == option),
                            None
                        )
                    else:
                        # Für die anderen beiden nehmen wir den alten Wert aus state
                        selected_value = next(
                            (entry.number for entry in item.resultlist if entry.translation_key == item.state),
                            None
                        )

                    if selected_value is not None:
                        selected_values[item.translation_key] = selected_value

            # Sicherstellen, dass alle drei Werte erfasst wurden
            if len(selected_values) != 3:
                raise ValueError(f"Erwartet 3 Werte, aber {len(selected_values)} erhalten: {selected_values}")

            # Werte in der richtigen Reihenfolge in Little-Endian umwandeln
            ordered_keys = ["absence_limit_max_waterflowrate", "absence_limit_max_water_flow", "absence_limit_max_waterflow_time"]
            payload = "".join([selected_values[key].to_bytes(2, byteorder="little").hex() for key in ordered_keys])

            # Debugging: Welche Werte wurden gesendet?
            log.debug("Gesammelte Werte für Little-Endian Umwandlung: %s", selected_values)
            log.debug("Sende Payload an Judo: %s", payload)
            
            try:
                if self._rest_item.translation_key in PERSISTENT_ENTITIES:
                    await save_last_written_value(self.hass, self._rest_item.translation_key, option)
                # Senden des kombinierten Zustands
                await self.coordinator.rest_api.write_value("5F00", bytes.fromhex(payload))
                self._rest_item.state = option
                self._attr_current_option = self._rest_item.state
                self.async_write_ha_state()
            except Exception as e:
                log.error("Fehler beim Senden an Judo: %s", e)
        
        #2 Special mode leakageprotection
        elif self._rest_item.translation_key in ["leakageprotection_max_waterflowrate", "leakageprotection_max_waterflow", "leakageprotection_max_waterflowtime"]:
            if not self.coordinator._restitems:
                raise ValueError("coordinator._restitems ist None oder leer. Keine Entitäten zum Verarbeiten.")

            # Lade gespeicherte Werte
            stored_values = await load_last_written_values(self.hass)
            selected_values = {}

            # Sammle alle benötigten Werte
            for key in ["holiday_mode_write", "leakageprotection_max_waterflowrate", "leakageprotection_max_waterflow", "leakageprotection_max_waterflowtime"]:
                if key == self._rest_item.translation_key:
                    # Für die aktuelle Entity nehmen wir den neuen Wert
                    selected_value = next(
                        (entry.number for entry in self._rest_item.resultlist if entry.translation_key == option),
                        None
                    )
                    if selected_value is not None:
                        # Speichere den neuen Wert
                        await save_last_written_value(self.hass, key, option)
                        log.debug("Gespeicherter Wert oben: %s", selected_value)
                else:
                    # Für die anderen Entities nehmen wir den gespeicherten Wert
                    stored_option = stored_values.get(key)
                    if stored_option:
                        # Finde den numerischen Wert für die gespeicherte Option
                        for item in self.coordinator._restitems:
                            if item.translation_key == key:
                                selected_value = next(
                                    (entry.number for entry in item.resultlist if entry.translation_key == stored_option),
                                    None
                                )
                                break

                if selected_value is not None:
                    selected_values[key] = selected_value

            # Debug Ausgabe
            log.debug("Gesammelte Werte für Leakageprotection: %s", selected_values)

            if len(selected_values) != 4:
                raise ValueError(f"Erwartet 4 Werte, aber {len(selected_values)} erhalten: {selected_values}")

            # Werte in der richtigen Reihenfolge in Little-Endian umwandeln
            ordered_keys = ["holiday_mode_write", "leakageprotection_max_waterflowrate", "leakageprotection_max_waterflow", "leakageprotection_max_waterflowtime",]
            #payload = "".join([selected_values[key].to_bytes(2, byteorder="little").hex() for key in ordered_keys])
            payload = ""
            for key in ordered_keys:
                if key == "holiday_mode_write":
                    payload += selected_values[key].to_bytes(1, byteorder="little").hex()
                else:
                    payload += selected_values[key].to_bytes(2, byteorder="little").hex()

            log.debug("Sende Leakageprotection Payload an Judo: %s", payload)
            
            try:
                if self._rest_item.translation_key in PERSISTENT_ENTITIES:
                    await save_last_written_value(self.hass, self._rest_item.translation_key, option)
                    logmeldung = (self.hass, self._rest_item.translation_key, option)
                    log.debug("Gespeicherter Wert unten: %s", logmeldung)
                # Senden des kombinierten Zustands
                await self.coordinator.rest_api.write_value("5000", bytes.fromhex(payload))
                self._rest_item.state = option
                self._attr_current_option = self._rest_item.state
                self.async_write_ha_state()
            except Exception as e:
                log.error("Fehler beim Senden an Judo: %s", e)
        else:
            try: #Speichern der Werte die nur geschrieben werden
                if self._rest_item.translation_key in PERSISTENT_ENTITIES:
                    await save_last_written_value(self.hass, self._rest_item.translation_key, option)
                    logmeldung = (self.hass, self._rest_item.translation_key, option)
                    log.debug("Gespeicherter Wert unten ohne Sonder: %s", logmeldung)

                #Daten aktuallisieren und schreiben
                ro = RestObject(self._rest_api, self._rest_item)
                await ro.setvalue(option)  # Use the RestObject setvalue method
                # Update the entity's state with the new value
                self._rest_item.state = option
                self._attr_current_option = self._rest_item.state
                self.async_write_ha_state()
            except Exception as e:
                log.error("Fehler beim Senden an Judo: %s", e)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_current_option = self._rest_item.state
        self.async_write_ha_state()
    
    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return MyEntity.my_device_info(self)
