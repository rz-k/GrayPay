import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

deposit_logger = logging.getLogger("deposit")
deposit_error_logger = logging.getLogger("deposit_error")
