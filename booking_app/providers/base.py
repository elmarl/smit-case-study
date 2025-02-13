from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict

class ServiceProviderAdapter(ABC):
    @abstractmethod
    async def fetch_available_times(self, from_date: datetime, until_date: datetime = None) -> List[Dict]:
        """
        Fetch available times from the provider and return them in a standardized format.
        """
        pass

    @abstractmethod
    async def book_time(self, booking_reference: str, contact_information: str) -> bool:
        """
        Book a time slot using the provider’s booking reference and contact information.
        """
        pass
