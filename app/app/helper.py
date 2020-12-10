import os
import re
import pkgutil
import logging as log
from functools import lru_cache
from datetime import datetime, timedelta

import pytz
from cryptography.fernet import Fernet


if not os.path.exists('key'):
    key = Fernet.generate_key()
    with open('key', 'wb') as f:
        f.write(key)

key = open('key', 'rb').read()
f = Fernet(key)


def get_modules(module, postfix=None):

    modules = []
    names = [name for f, name, ispkg in pkgutil.iter_modules(module.__path__)]

    for name in names:
        package_name = f"{module.__name__}.{name}"
        module_name = name if postfix is None else f'{name}_{postfix}'
        _module = (module_name, __import__(package_name, fromlist=[name]))
        modules.append(_module)

    return modules


def get_current():
    tz = pytz.timezone('Asia/Tehran')
    return datetime.now(tz)


def get_last_month():
    current = get_current()
    first = current.replace(day=1)
    last_month = first - timedelta(days=1)

    return last_month


def get_expiration(days=30):
    dt = get_current()
    delta = timedelta(days)
    expiration_date = dt + delta
    log.debug(expiration_date)
    return expiration_date


def std_date(dt):
    if isinstance(dt, str):
        dt = datetime.strptime(dt, '%Y-%m-%d')
    current = get_current()
    return dt.replace(tzinfo=current.tzinfo)


@lru_cache
def persian_numbers(number):

    @lru_cache
    def convert(x):
        return u'۰۱۲۳۴۵۶۷۸۹'[int(x.group(0))]

    return re.sub('[0-9]', convert, str(number))


@lru_cache
def percent(value, total):
    return '{0:.2f}'.format(100 * float(value) / float(total))


def string_encrypt(data):
    return f.encrypt(data.encode('utf-8'))


def string_decrypt(data):
    return f.decrypt(bytes(data, encoding='utf-8'))


def get_id(_):
    return int(_.string_decrypt(_.request.args.get('id')))


def put_id(_, _id):
    return _.string_encrypt(str(_id))
