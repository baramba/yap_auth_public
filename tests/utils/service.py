import email
import os
from typing import Union

import psycopg2
from dotenv import load_dotenv
from pydantic import BaseModel

from tests.utils.structures import User

load_dotenv()


def validate(
    data: Union[list[Union[bytes, dict]], Union[bytes, dict]], model: BaseModel
) -> Union[list[BaseModel], BaseModel]:
    if isinstance(data, list):
        if isinstance(data[0], dict):
            return [model.parse_obj(item) for item in data]
        if isinstance(data[0], bytes):
            return [model.parse_raw(item) for item in data]
    else:
        if isinstance(data, dict):
            return model.parse_obj(data)
        if isinstance(data, bytes):
            return model.parse_raw(data)


def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('POSTGRES_HOST'),
        database=os.environ.get('POSTGRES_DB'),
        user=os.environ.get('POSTGRES_USER'),
        password=os.environ.get('POSTGRES_PASSWORD')
    )
    return conn


def del_user(user: User):
    conn = get_db_connection()
    cur = conn.cursor()
    print('Before del:')
    cur.execute('''SELECT * FROM users;''')
    res = cur.fetchall()
    for item in res:
        print(item)
    sql = '''
        DELETE FROM users WHERE email = '{email}';
    '''
    cur.execute(sql.format(email=user.email))
    print('After del:')
    cur.execute('''SELECT * FROM users;''')
    res = cur.fetchall()
    for item in res:
        print(item)
    cur.close()
    conn.close()
