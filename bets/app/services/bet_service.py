from datetime import datetime

from app.services.executor import execute_insert
from app.services.executor import execute_update
from app.services.executor import execute_select
from app.services.executor import execute_delete

from sqlalchemy.exc import IntegrityError


def create(bet):
    if bet.user_id is None or bet.event_id is None or bet.market is None:
        return {"error": "user_id, event_id and market fields are required"}

    event_query = f'''
    SELECT id, state, score
    FROM public."Events"
    WHERE id = {bet.event_id};
    '''
    try:
        event = execute_select(event_query)[0]
    except IntegrityError:
        return {"error": "no event with such id"}
    except ValueError as e:
        return {"error": str(e)}


    state = 'losing'

    if event['state'] == 'created':
        state = 'none'
    elif event['state'] == 'finished':
        return {"error": "event is already finished"}
    elif event['state'] == 'active':
        score = event['score'].split("-")
        if (score[0] == score[1] and bet.market == 'draw') or \
                (score[0] > score[1] and bet.market == 'team_1') or \
                (score[1] > score[0] and bet.market == 'team_2'):
            state = 'winning'

    bet.market = f"'{bet.market}'"
    sql_first_part = 'INSERT INTO public."Bets"(data_created, state'
    sql_second_part = f'VALUES (\'{datetime.now().strftime("%Y-%m-%d")}\', \'{state}\''
    for property, value in bet.dict(exclude_none=True).items():
        sql_first_part += f', {property}'
        sql_second_part += f', {value}'
    sql_query = sql_first_part + ') ' + sql_second_part + ') RETURNING id;'

    try:
        result = execute_insert(sql_query)
    except IntegrityError:
        return {"error": "no user with such id"}

    return {"id": result}


def update(bet):
    if bet.id is None:
        return {"error": "id field is required"}

    sql_query = 'UPDATE public."Bets" SET '
    for property, value in bet.dict(exclude_none=True).items():
        sql_query += f'{property} = {value}, '

    sql_query = sql_query[:-2] + f' WHERE id = {bet.id} RETURNING *'

    try:
        result = execute_update(sql_query)
    except ValueError as e:
        return {"error": str(e)}
    except IntegrityError:
        return {"error": "no user or event with such id"}
    return {"updated_user": result}


def get_by_id(id):
    sql_query = f'''
    SELECT id, data_created, user_id, event_id, market, state
    FROM public."Bets"
    WHERE id = {id};
    '''

    try:
        result = execute_select(sql_query)
    except ValueError as e:
        return {"error": str(e)}
    return result


def get_all():
    sql_query = f'''
    SELECT id, data_created, user_id, event_id, market, state
    FROM public."Bets";
    '''

    try:
        result = execute_select(sql_query)
    except ValueError:
        return {"error": 'have no bets;('}
    return result


def delete_by_id(id):
    sql_query = f'''
    DELETE FROM public."Bets"
    WHERE id = {id}
    RETURNING id;
    '''

    try:
        result = execute_delete(sql_query)
    except ValueError as e:
        return {"error": str(e)}
    return {f"bet{result['id']}": "is deleted"}
