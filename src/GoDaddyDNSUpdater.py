import requests
from dotenv import dotenv_values

from .DNSUpdater import DNSUpdater
from .Logger import Logger

class GoDaddyDNSUpdater(DNSUpdater):
    def __init__(self, domain: str, logger: Logger):
        self.logger = logger
        
        # Load the environment variables
        env_vars = dotenv_values()
        
        self.godaddy_api_key = env_vars['GODADDY_API_KEY']
        """The API key for the GoDaddy API"""

        self.godaddy_api_secret = env_vars['GODADDY_API_SECRET']
        """The API secret for the GoDaddy API"""

        self.domain = domain
        """The domain to change the DNS records for"""
            
        self.godaddy_api_url = f"https://api.godaddy.com/v1/domains/{self.domain}/records"
        """The URL to use for the GoDaddy API requests"""

    def update_dns(self, new_ip: str):
        headers = {
            "Authorization": f"sso-key {self.godaddy_api_key}:{self.godaddy_api_secret}",
            "Content-Type": "application/json"
        }

        # Define the A record update request
        a_record = [{
            "type": "A",
            "name": '@',
            "data": new_ip,
            "ttl": 600 # 600 seconds (previous A record TTL)
        }]

        a_request_url = f'{self.godaddy_api_url}/A/@'

        self.logger.log_message(f"Updating A record using {a_request_url} with data {a_record}")

        # Update the CNAME record
        response_a = requests.put(a_request_url, headers=headers, json=a_record)

        if response_a.status_code == 200:
            self.logger.log_message("A record updated successfully.")
        else:
            self.logger.log_message(f"Failed to update A record. Status Code: {response_a.status_code}")
            self.logger.log_message("Response:", response_a.text)