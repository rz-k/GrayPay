import threading
from uuid import uuid4

import requests
from django.utils.timezone import now

from utils.load_env import env
from utils.logger import logger


def update_object(obj, **kwargs) -> None:
    """
    Update object attributes in the database.
    """
    if kwargs:
        obj.__class__.objects.filter(pk=obj.pk).update(**kwargs)

def generate_payment_id():
    """
    Generates a unique payment id in format:
    PAY-YYYYMMDD-XXXXXX
    """
    date_str = now().strftime("%Y%m%d")
    uid = str(uuid4())[:6].upper()
    return f"PAY-{date_str}-{uid}"

def run_function_in_thread(func, *args, **kwargs):
    """
        Run the given function in a separate thread.
    """
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread

def build_payment_message(payment):
    return (
        "💳 <b>New Payment</b>\n\n"
        f"👤 Name: <b>{payment.full_name}</b>\n"
        f"📞 Phone: <b>{payment.phone}</b>\n"
        f"💰 Amount: <b>{payment.amount:,} Toman</b>\n"
        f"🆔 Authority: <code>{payment.authority}</code>\n"
        f"📦 Order ID: <code>{payment.order_id}</code>\n"
        f"📝 Description: <b>{payment.description}</b>\n"
    )

def send_payment_to_telegram(payment):
    proxy = None
    if env.get("PROXY_SOCKS"):
        proxy = {
            "http": f"socks5h://{env.get('PROXY_SOCKS')}",
            "https": f"socks5h://{env.get('PROXY_SOCKS')}",
        }

    url = f"https://api.telegram.org/bot{env.get('TOKEN')}/sendMessage"
    payload = {
        "chat_id": env.get("ACTION_CHANNEL"),
        "text": build_payment_message(payment),
        "parse_mode": "html",
    }

    try:
        response = requests.get(
            url,
            params=payload,
            proxies=proxy,
            timeout=15
        )
        response.raise_for_status()

    except Exception:
        logger.error(
            "Telegram notification failed for payment %s",
            payment.id
        )
