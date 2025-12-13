import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)



withdraw_logger = logging.getLogger("withdraw")
withdraw_success_logger = logging.getLogger("withdraw_success")
deposit_logger = logging.getLogger("deposit")
deposit_error_logger = logging.getLogger("deposit_error")
system_logger = logging.getLogger("system")
