import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .api import FoxESSApi,FoxESSApiError
from .const import DOMAIN,CONF_API_KEY,CONF_DEVICE_SN
class ConfigFlow(config_entries.ConfigFlow,domain=DOMAIN):
    VERSION=1
    async def async_step_user(self,user_input=None):
        errors={}
        if user_input:
            api=FoxESSApi(user_input[CONF_API_KEY].strip(),user_input[CONF_DEVICE_SN].strip(),async_get_clientsession(self.hass))
            try: await api.get_export_limit()
            except FoxESSApiError: errors["base"]="cannot_connect"
            except Exception: errors["base"]="unknown"
            else:
                await self.async_set_unique_id(user_input[CONF_DEVICE_SN].strip().lower())
                self._abort_if_unique_id_configured()
                return self.async_create_entry(title=f"FoxESS {user_input[CONF_DEVICE_SN].strip()}",data={CONF_API_KEY:user_input[CONF_API_KEY].strip(),CONF_DEVICE_SN:user_input[CONF_DEVICE_SN].strip()})
        return self.async_show_form(step_id="user",data_schema=vol.Schema({vol.Required(CONF_API_KEY):str,vol.Required(CONF_DEVICE_SN):str}),errors=errors)
