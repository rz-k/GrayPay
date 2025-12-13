import random
import threading
from decimal import Decimal
from uuid import uuid4

from django.utils.timezone import now


def update_object(obj, **kwargs) -> None:
    """
    Update object attributes in the database.
    """
    if kwargs:
        obj.__class__.objects.filter(pk=obj.pk).update(**kwargs)


def decimal_rounded_average_score(number):
    average_score = Decimal(number)
    rounded_average_score = average_score.quantize(Decimal("0.00"))
    return rounded_average_score


def generate_payment_id():
    """
    Generates a unique payment id in format:
    PAY-YYYYMMDD-XXXXXX
    """
    date_str = now().strftime("%Y%m%d")
    uid = str(uuid4())[:6].upper()
    return f"PAY-{date_str}-{uid}"


def assign_boxes():
    numbers = list(range(1, 11))
    random.shuffle(numbers)

    bombs = numbers[:6]
    safe = numbers[6:8]
    prizes = numbers[8:]
    result = {}
    for n in bombs:
        result[n] = "bomb"
    for n in safe:
        result[n] = "safe"
    for n in prizes:
        result[n] = "prize"

    return result

def run_function_in_thread(func, *args, **kwargs):
    """
        Run the given function in a separate thread.
    """
    thread = threading.Thread(target=func, args=args, kwargs=kwargs)
    thread.start()
    return thread
