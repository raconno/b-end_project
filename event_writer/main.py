from kafka import KafkaConsumer
import logging
from sqlalchemy import create_engine
from sqlalchemy import text
import json

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@db:5432/app'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

consumer = KafkaConsumer('events.taxonomy', bootstrap_servers=['broker:29092'], group_id='event_writer')

def create(event_dict):
    sql_first_part = 'INSERT INTO public."Events"( state, score'
    sql_second_part = f'VALUES ( \'created\', \'0-0\''
    for property, value in event_dict.items():
        sql_first_part += f', {property}'
        sql_second_part += f', {value}'

    sql_query = sql_first_part + ') ' + sql_second_part + ') RETURNING *;'

    result = engine.execute(sql_query)
    logging.log(1, result.first()[0])


def update(event):

    sql_query = 'UPDATE public."Events" SET '
    for property, value in event.items():
        sql_query += f'{property} = {value}, '
    sql_query = sql_query[:-2]
    sql_query += f' WHERE id = {event["id"]} RETURNING *'

    result = engine.execute(text(sql_query))
    result = result.first()
    logging.log(1, result)
    if not result:
        raise ValueError('no event with such id')


for msg in consumer:
    if msg.key.decode("utf-8").startswith('create'):
        logging.warning("event_writer: " + str(json.loads(msg.value)))
        create(json.loads(msg.value))
    elif msg.key.decode("utf-8").startswith('update'):
        logging.warning("event_writer: " + str(json.loads(msg.value)))
        update(json.loads(msg.value))
    else:
        raise KeyError("event_writer: should start with 'create' or 'update'.'" + str(msg.key) + "' not available")
