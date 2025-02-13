import json
from .providers.provider_one import ProviderOneAdapter
from .providers.provider_two import ProviderTwoAdapter

class ProviderRegistry:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as f:
            self.providers_config = json.load(f)
        self.adapters = self._load_adapters()

    def _load_adapters(self):
        adapters = {}
        adapter_classes = {
            "ProviderOneAdapter": ProviderOneAdapter,
            "ProviderTwoAdapter": ProviderTwoAdapter,
        }
        for config in self.providers_config:
            adapter_class = adapter_classes.get(config["adapter"])
            if adapter_class:
                adapters[config["id"]] = adapter_class(config["base_url"], config["supported_vehicle_types"])
        return adapters

    def get_all_adapters(self):
        return self.adapters.values()

    def get_adapter(self, provider_id: str):
        return self.adapters.get(provider_id)
