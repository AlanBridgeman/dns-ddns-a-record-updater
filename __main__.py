import sys, os, socket

from src.Logger import Logger
from src.DNSUpdater import DNSUpdater

def main(dns_domain: str, ddns_domain: str, dns_provider='GoDaddy', log_filename: str = '/var/log/dns_updater.log', log_level: str = 'INFO'):
    """Entrypoint for the script

    Args:
        dns_domain (str): The domain to update the DNS records for
        ddns_domain (str): The domain to get the IP address from
        dns_provider (str, optional): The DNS provider, needed to know how to update the record. Defaults to 'GoDaddy'.
        log_filename (str, optional): The filename to use for the log file. Defaults to '/var/log/dns_updater.log'.
        log_level (str, optional): The log level to use. Defaults to 'INFO'.
    """

    logger = Logger(filename=log_filename, log_level=log_level)

    dns_ip = socket.gethostbyname(dns_domain)
    ddns_ip = socket.gethostbyname(ddns_domain)
    if dns_ip != ddns_ip:
        logger.log_message('Need to update DNS from ' + dns_ip + ' to ' + ddns_ip)

        updater: DNSUpdater = None
        
        if dns_provider == 'GoDaddy':
            from src.GoDaddyDNSUpdater import GoDaddyDNSUpdater
            updater = GoDaddyDNSUpdater(dns_domain, logger)
        
        # Update the DNS
        updater.update_dns(ddns_ip)
    else:
        logger.log_message('DNS is up to date!')

if __name__ == '__main__':
    # Error if no .env file is found
    if not os.path.exists('.env'):
        print('No .env file found. Please create one with the required environment variables.')
        exit(1)

    # Verify that we only have 3 or 4 arguments
    if not len(sys.argv) < 3 and len(sys.argv) > 6:
        print('Usage: python . <GoDaddy_domain_to_update> <Dynamic_DNS_domain> [DNS_provider (optional)] [log_filename (optional)] [log_level (optional)]')
        exit(1)
    
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])