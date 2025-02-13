import httpx
from datetime import datetime, timezone
from typing import List, Dict
from .base import ServiceProviderAdapter

class ProviderTwoAdapter(ServiceProviderAdapter):
    def __init__(self, base_url: str, supported_vehicle_types: str):
        self.base_url = base_url
        self.supported_vehicle_types = supported_vehicle_types

    async def fetch_available_times(self, from_date: datetime, until_date: datetime = None) -> List[Dict]:
        params = {"from": from_date.strftime("%Y-%m-%d")}
        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url, params=params)
        
        data = response.json()
        available_times = []
        for item in data:
            if item.get("available"):
                time_str = item.get("time")
                item_time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))
                
                # filtering out in-memory since the api does not support until_date filtering.
                item_time = datetime.fromisoformat(time_str.replace("Z", "+00:00"))        
                if until_date:
                    if until_date.tzinfo is None:
                        until_date = until_date.replace(tzinfo=timezone.utc)
                    if item_time > until_date:
                        continue
                
                available_times.append({
                    "provider_id": "provider_two",
                    "time": time_str,
                    "booking_reference": str(item.get("id")),
                    "vehicle_types": self.supported_vehicle_types
                })
        return available_times

    async def book_time(self, booking_reference: str, contact_information: str) -> bool:
        payload = {"contactInformation": contact_information}
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{self.base_url}/{booking_reference}/booking", 
                                         json=payload, 
                                         headers={"Content-Type": "application/json"})
        return response.status_code in (200, 201, 204)
