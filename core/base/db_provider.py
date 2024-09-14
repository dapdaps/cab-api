import decimal
import json
from datetime import datetime
import psycopg2
from settings.config import DATABASE_HOST, DATABASE_NAME, DATABASE_USERNAME, DATABASE_PASSWORD
from tortoise.transactions import in_transaction


class Encoder(json.JSONEncoder):
    """
    Handle special data types, such as decimal and time types
    """

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)

        if isinstance(o, datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S")

        super(Encoder, self).default(o)


def get_db_connect():
    conn = psycopg2.connect(
        database=DATABASE_NAME,
        user=DATABASE_USERNAME,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=5432)
    return conn


async def start_transaction(fun):
    async with in_transaction(connection_name='default') as connection:
        return await fun(connection)


if __name__ == '__main__':
    print("#########START MAIN###########")

