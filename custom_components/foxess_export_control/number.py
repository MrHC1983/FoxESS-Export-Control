import logging
from homeassistant.components.number import NumberEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity,DataUpdateCoordinator,UpdateFailed
from .api import FoxESSApi,FoxESSApiError
from .const import *
_LOGGER=logging.getLogger(__name__)
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry,async_add_entities:AddEntitiesCallback):
    api=FoxESSApi(entry.data[CONF_API_KEY],entry.data[CONF_DEVICE_SN],async_get_clientsession(hass))
    async def update():
        try:return await api.get_export_limit()
        except FoxESSApiError as e:raise UpdateFailed(str(e)) from e
    coordinator=DataUpdateCoordinator(hass,_LOGGER,name=f"FoxESS Export Limit {entry.data[CONF_DEVICE_SN]}",update_method=update,update_interval=None)
    await coordinator.async_config_entry_first_refresh()
    async_add_entities([FoxESSExportLimitNumber(coordinator,api,entry)])
class FoxESSExportLimitNumber(CoordinatorEntity,NumberEntity):
    _attr_has_entity_name=True
    _attr_translation_key="export_limit"
    _attr_native_unit_of_measurement=UnitOfPower.WATT
    _attr_native_min_value=MIN_EXPORT_LIMIT
    _attr_native_max_value=MAX_EXPORT_LIMIT
    _attr_native_step=EXPORT_STEP
    _attr_mode="box"
    def __init__(self,coordinator,api,entry):
        super().__init__(coordinator); self._api=api; self._attr_unique_id=f"{entry.data[CONF_DEVICE_SN].lower()}_export_limit"
    @property
    def native_value(self): return self.coordinator.data
    async def async_set_native_value(self,value:float):
        value=max(MIN_EXPORT_LIMIT,min(MAX_EXPORT_LIMIT,int(round(value/EXPORT_STEP)*EXPORT_STEP)))
        await self._api.set_export_limit(value); self.coordinator.async_set_updated_data(value)
