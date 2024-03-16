from abc import ABC, abstractmethod

class DNSUpdater(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def update_dns(self, ip):
        pass