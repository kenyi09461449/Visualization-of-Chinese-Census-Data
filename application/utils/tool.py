import datetime
import json
import time
import hashlib
from ..config.config import DATABASE
from simple_mysql import db as mysql


# customer json encoder
class NewEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%I:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)


def get_db():
    """
    get database
    :return:
    """
    return mysql().connection(DATABASE)


def logger(user: int, type: str, content: str):
    """
    save log
    :return:
    """
    db = get_db()
    res = db.table('logs').add({
        "user_id": user,
        "content": content,
        "type": type,
        'create_at': get_date_time(),
    })
    return res


def jsonResponse(code=500, msg='error', data=None):
    """
        format json
    """
    if data is None:
        data = []
    return json.dumps({"code": code, "msg": msg, "data": data}, cls=NewEncoder)


def md5(string=''):
    """
    md5 function
    """
    if not string:
        return
    return hashlib.md5(string.encode("utf-8")).hexdigest()


def get_date():
    """
    get today date
    :return:
    """
    return time.strftime('%Y-%m-%d', time.localtime())


def get_date_time():
    """
    get current time
    :return:
    """
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
