import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict
from .base import ServiceProviderAdapter

class ProviderOneAdapter(ServiceProviderAdapter):
    def __init__(self, base_url: str, supported_vehicle_types: str):
        self.base_url = base_url
        self.supported_vehicle_types = supported_vehicle_types

    async def fetch_available_times(self, from_date: datetime, until_date: datetime) -> List[Dict]:
        params = {
            "from": from_date.strftime("%Y-%m-%d"),
            "until": until_date.strftime("%Y-%m-%d")
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/available", params=params)
        
        root = ET.fromstring(response.text)
        available_times = []
        for time_slot in root.findall(".//availableTime"):
            time_str = time_slot.find("time").text
            uuid = time_slot.find("uuid").text
            available_times.append({
                "provider_id": "provider_one",
                "time": time_str,
                "booking_reference": uuid,
                "vehicle_types": self.supported_vehicle_types
            })
        return available_times

    async def book_time(self, booking_reference: str, contact_information: str) -> bool:
        xml_body = f"""<?xml version="1.0" encoding="UTF-8"?>
<london.tireChangeBookingRequest>
    <contactInformation>{contact_information}</contactInformation>
</london.tireChangeBookingRequest>
"""
        async with httpx.AsyncClient() as client:
            response = await client.put(
                f"{self.base_url}/{booking_reference}/booking",
                data=xml_body,
                headers={"Content-Type": "application/xml"}
            )
        return response.status_code in (200, 204)