from kafka import KafkaConsumer, KafkaProducer
from sqlalchemy import create_engine
from sqlalchemy import text
import logging
import json

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@db:5432/app'
engine = create_engine(SQLALCHEMY_DATABASE_URL)

def serializer(value):
    return json.dumps(value).encode()

consumer = KafkaConsumer('events.taxonomy', bootstrap_servers=['broker:29092'], group_id='bet_scorer')
producer = KafkaProducer(bootstrap_servers='broker:29092', value_serializer=serializer)


def produce(key, value):
    producer.send('bets.state', value=value, key=str(key).encode())
    producer.flush()


def parse_score(score):
    score = score[1:-1].split("-")
    team_1 = int(score[0])
    team_2 = int(score[1])
    if team_1 == team_2:
        score = 'draw'
    elif team_1 > team_2:
        score = 'team_1'
    else:
        score = 'team_2'
    return score


def execute_select(sql_query):
    res = engine.execute(text(sql_query))
    result = []
    for row in res:
        result.append(row)
    if not result:
        raise ValueError('no row with such id')
    return result


def select_bets_with_event(id):
    sql_query = f'''
    SELECT id, market, state
    FROM public."Bets"
    WHERE event_id = {id};'''
    logging.warning("sql_query: " + sql_query)
    return execute_select(sql_query)


def update_bets(event):
    try:
        logging.warning("event[\"id\"]: " + event["id"])
        bets = select_bets_with_event(event["id"])
        logging.warning("betsss: " + str(bets))
    except ValueError:
        return None
    score = parse_score(event["score"])
    logging.warning("score: " + str(type(score)) + "  " + str(score))
    for bet in bets:
        logging.warning("bet[\"market\"]: " + str(type(bet["market"])) + "  " + str(bet["market"]))
        if bet["market"] == score:
            bet_state = 'winning'
        else:
            bet_state = 'losing'
        logging.warning("bet_state: " + str(bet_state))
        if bet_state != bet["state"]:
            # sql_query = f'UPDATE public."Bets" SET state = \'{bet_state}\' WHERE id = {bet["id"]}'
            # engine.execute(text(sql_query))
            produce(bet["id"], {"id": bet["id"], "state": bet_state})

def finish_event(event):
    try:
        bets = select_bets_with_event(event["id"])
    except ValueError:
        return None

    score = event.get("score")
    if not score:
        sql_query = f'''
        SELECT state
        FROM public."Events"
        WHERE id = {event["id"]};
        '''
        score = execute_select(sql_query)[0][0]

    score = parse_score(score)
    for bet in bets:
        if bet["market"] == score:
            bet_state = 'win'
        else:
            bet_state = 'lose'
        produce(bet["id"], {"id": bet["id"], "state": bet_state})



for msg in consumer:
    if msg.key.decode("utf-8").startswith('update') and json.loads(msg.value).get("state") == "finished":
        logging.warning("bet_scorer: " + str(json.loads(msg.value)))
        finish_event(json.loads(msg.value))
    elif msg.key.decode("utf-8").startswith('update') and json.loads(msg.value).get("score"):
        logging.warning("bet_scorer: " + str(json.loads(msg.value)))
        update_bets(json.loads(msg.value))
