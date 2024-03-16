import logging, time

class Logger:
    def __init__(self, filename: str = '/var/log/dns_updater.log', log_level: str = 'INFO'):
        logging.basicConfig(filename=filename, level=logging.getLevelName(log_level))
    
    def log_message(self, message: str, level: str = 'DEBUG'):
        curr_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        
        if level == 'DEBUG':
            logging.debug('[' + curr_time + ']: ' + message)
        elif level == 'INFO':
            logging.info('[' + curr_time + ']: ' + message)
        elif level == 'WARNING':
            logging.warning('[' + curr_time + ']: ' + message)
        elif level == 'ERROR':
            logging.error('[' + curr_time + ']: ' + message)
        elif level == 'CRITICAL':
            logging.critical('[' + curr_time + ']: ' + message)
        else:
            print('[' + curr_time + ']: ' + message)