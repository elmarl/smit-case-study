from fastapi import FastAPI, Query, HTTPException
from datetime import datetime
import asyncio
from pydantic import BaseModel
from registry import ProviderRegistry

class BookingRequest(BaseModel):
    contactInformation: str

app = FastAPI(title="Tire Change Booking API")
# can add sentry error logging in the future here.
# app.add_middleware(SentryAsgiMiddleware)
provider_registry = ProviderRegistry("providers_config.json")

@app.get("/available-times")
async def get_available_times(
    from_date: datetime = Query(..., alias="from"),
    until_date: datetime = Query(None, alias="until"),
    provider: str = Query(None),
    vehicle_type: str = Query(None)
):
    adapters = list(provider_registry.get_all_adapters())
    if provider:
        adapter = provider_registry.get_adapter(provider)
        if not adapter:
            raise HTTPException(status_code=404, detail="Provider not found")
        adapters = [adapter]
    
    tasks = [
        adapter.fetch_available_times(from_date, until_date or datetime.max)
        for adapter in adapters
    ]
    results = await asyncio.gather(*tasks)
    
    available_times = [time for sublist in results for time in sublist]
    
    if vehicle_type:
        available_times = [
            t for t in available_times if vehicle_type in t["vehicle_types"]
        ]
    
    return available_times

@app.post("/book/{provider_id}/{booking_reference}")
async def book_time(provider_id: str, booking_reference: str, booking_request: BookingRequest):
    adapter = provider_registry.get_adapter(provider_id)
    if not adapter:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    success = await adapter.book_time(booking_reference, booking_request.contactInformation)
    if success:
        return {"status": "booked"}
    raise HTTPException(status_code=400, detail="Booking failed")
