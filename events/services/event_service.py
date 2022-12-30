from datetime import datetime

from services.produce_kafka import produce
from services.executor import execute_select
from services.executor import execute_delete


def _format_value(property, value):
    if property == 'event_date':
        try:
            value = datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("should be a date in format '%Y-%m-%d'")
        return f'\'{value}\''
    elif value:
        return f'\'{value}\''
    else:
        return 'NULL'


def create(event):

    if event.type is None or event.team_1 is None or event.team_2 is None or event.event_date is None:
        return {"error": "type, event_date, team_1 and team_2 fields are required"}

    event_dict = event.dict(exclude_none=True)
    for property, value in event_dict.items():
        event_dict[property] = _format_value(property, value)

    produce(f"create{event.event_date}", event_dict)


def update(event):
    if event.id is None:
        return {"error": "id field is required"}

    event_dict = event.dict(exclude_none=True)
    for property, value in event_dict.items():
        event_dict[property] = _format_value(property, value)

    produce(f"update{event.id}", event_dict)


def get_by_id(id):
    sql_query = f'''
    SELECT id, type, team_1, team_2, event_date, score, state
    FROM public."Events"
    WHERE id = {id};
    '''

    try:
        result = execute_select(sql_query)
    except ValueError as e:
        return {"error": str(e)}
    return result


def get_all():
    sql_query = f'''
    SELECT id, type, team_1, team_2, event_date, score, state
    FROM public."Events";
    '''

    try:
        result = execute_select(sql_query)
    except ValueError:
        return {"error": 'have no events;('}
    return result


def delete_by_id(id):
    sql_query = f'''
    DELETE FROM public."Events"
    WHERE id = {id}
    RETURNING id;
    '''

    try:
        result = execute_delete(sql_query)
    except ValueError as e:
        return {"error": str(e)}
    return {f"event{result['id']}": "is deleted"}
