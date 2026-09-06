import hashlib,time
from typing import Any
import aiohttp
from .const import API_BASE,SETTING_GET,SETTING_SET,SETTING_KEY
class FoxESSApiError(Exception): pass
class FoxESSApi:
    def __init__(self,api_key:str,device_sn:str,session:aiohttp.ClientSession):
        self.api_key=api_key; self.device_sn=device_sn; self.session=session
    def _headers(self,path:str):
        timestamp=str(int(time.time()*1000))
        text=f"{path}\r\n{self.api_key}\r\n{timestamp}"
        return {"Content-Type":"application/json","token":self.api_key,"timestamp":timestamp,"signature":hashlib.md5(text.encode()).hexdigest(),"lang":"en"}
    async def _post(self,path:str,body:dict[str,Any]):
        try:
            async with self.session.post(f"{API_BASE}{path}",json=body,headers=self._headers(path),timeout=aiohttp.ClientTimeout(total=15)) as r:
                data=await r.json(content_type=None)
        except Exception as e: raise FoxESSApiError(f"FoxESS Cloud request failed: {e}") from e
        if r.status!=200: raise FoxESSApiError(f"FoxESS Cloud HTTP {r.status}: {data}")
        if data.get("errno",0)!=0: raise FoxESSApiError(f"FoxESS Cloud error {data.get('errno')}: {data.get('msg','Unknown error')}")
        return data
    async def get_export_limit(self)->int:
        data=await self._post(SETTING_GET,{"sn":self.device_sn,"key":SETTING_KEY})
        result=data.get("result")
        value=result.get("value") if isinstance(result,dict) else result
        if value is None: raise FoxESSApiError("FoxESS did not return an ExportLimit value")
        return int(float(value))
    async def set_export_limit(self,value:int)->None:
        await self._post(SETTING_SET,{"sn":self.device_sn,"key":SETTING_KEY,"value":str(int(value))})
