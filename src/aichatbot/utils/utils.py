import os
import shutil
import re
import secrets
import string
from datetime import datetime
from .. import logger
from os.path import join, dirname, abspath


def gen_random_unique_string(product_code, length: int = 0):
    if length:
        random_str = ''.join((secrets.choice(string.digits) for x in range(length)))
        code = random_str
    else:
        random_str = ''.join((secrets.choice(string.digits) for x in range(10)))
        code = str(random_str) + str(product_code)
    return code


def clear_folder(path):
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def ensure_trailing_slash(url):
    return os.path.join(url, '')


def get_current_date_time():
    res_date_time = datetime.utcnow().strptime(datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%fZ"), "%Y-%m-%dT%H:%M:%S.%fZ")
    return res_date_time


def convert_str_to_iso_datetime(data_str):
    try:
        date_time_obj = datetime.strptime(data_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return date_time_obj, None
    except Exception as e:
        return None, e


def convert_datetime_to_iso(date_obj):
    try:
        date_str = date_obj.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        iso_date = convert_str_to_iso_datetime(str(date_str))
        return iso_date[0], None
    except Exception as e:
        return None, e


def success_response_w_pagination(body, pagination):
    res = {
        'data': body,
        'pagination': {
            'page_size': pagination['page_size'],
            'page_number': pagination['page_number'],
            'total': pagination['total'],
        },
        "detail": []
    }
    return res


def success_response(body):
    res = {
        'data': body,
        "detail": []
    }
    return res


def failure_response(err):
    logger.error(str(err))
    errs = [
        {
            'msg': str(err),
        }
    ]
    return errs


def failure_response_kit_registration(err, remain_attempts=None):
    logger.error(str(err))
    if remain_attempts is not None:
        errs = [
            {
                'msg': str(err),
                'remain_attempts': int(remain_attempts)
            }
        ]
    else:
        errs = [
            {
                'msg': str(err)
            }
        ]
    return errs


def validate_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False
