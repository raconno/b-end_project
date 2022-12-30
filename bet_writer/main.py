from kafka import KafkaConsumer
import logging
from sqlalchemy import create_engine
from sqlalchemy import text
import json

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@db:5432/app'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

consumer = KafkaConsumer('bets.state', bootstrap_servers=['broker:29092'], group_id='bet_writer')


def update(bet):
    sql_query = f'UPDATE public."Bets" SET state = \'{bet["state"]}\' WHERE id = {bet["id"]} RETURNING id'
    result = engine.execute(text(sql_query))
    result = result.first()
    logging.log(1, result)
    if not result:
        raise ValueError('no bet with such id')


for msg in consumer:
    logging.warning("bet_writer: " + str(json.loads(msg.value)))
    update(json.loads(msg.value))
