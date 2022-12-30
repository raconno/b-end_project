from sqlalchemy import create_engine
from sqlalchemy import text
import logging

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@db:5432/app'
DATABASE_NAME = 'app'
engine = create_engine(SQLALCHEMY_DATABASE_URL)


def execute_create(sql) -> None:
    engine.execute(text(sql))


def execute_insert(sql):
    result = engine.execute(text(sql))
    return result.first()[0]


def execute_update(sql):
    result = engine.execute(text(sql))
    result = result.first()
    logging.warning(result)
    if not result:
        raise ValueError('no row with such id')
    return result


def execute_select(sql):
    res = engine.execute(text(sql))
    result = []
    for row in res:
        result.append(row)
    if not result:
        raise ValueError('no row with such id')
    return result


def execute_delete(sql):
    result = engine.execute(text(sql))
    result = result.first()
    if not result:
        raise ValueError('no row with such id')
    return result
