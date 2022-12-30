from datetime import datetime

from app.services.executor import execute_insert
from app.services.executor import execute_update
from app.services.executor import execute_select
from app.services.executor import execute_delete


def _format_value(value):
    if type(value) == int:
        return value
    elif value:
        return f'\'{value}\''
    else:
        return 'NULL'


def create(user):
    if user.name is None and user.age is None:
        return {"error": "name and age fields are required"}
    elif user.name is None:
        return {"error": "name field is required"}
    elif user.age is None:
        return {"error": "age field is required"}

    sql_first_part = 'INSERT INTO public."Users"(time_created'
    sql_second_part = f'VALUES (\'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\''

    for property, value in user.dict(exclude_none=True).items():
        sql_first_part += f', {property}'
        sql_second_part += f', {_format_value(value)}'

    sql_query = sql_first_part + ') ' + sql_second_part + ') RETURNING id;'

    return {"id": execute_insert(sql_query)}


def update(user):
    if user.id is None:
        return {"error": "id field is required"}

    sql_query = 'UPDATE public."Users" SET '

    for property, value in user.dict(exclude_none=True).items():
        sql_query += f'{property} = {_format_value(value)}, '

    sql_query = sql_query[:-2]
    sql_query += f' WHERE id = {user.id} RETURNING *'

    try:
        result = execute_update(sql_query)
    except ValueError as e:
        return {"error": str(e)}
    return {"updated_user": result}


def get_by_id(id):
    sql_query = f'''
    SELECT id, name, last_name, time_created, gender, age, city, birth_day, premium, ip
    FROM public."Users"
    WHERE id = {id};
    '''

    try:
        result = execute_select(sql_query)
    except ValueError as e:
        return {"error": str(e)}
    return result


def get_all():
    sql_query = f'''
    SELECT id, name, last_name, time_created, gender, age, city, birth_day, premium, ip
    FROM public."Users";
    '''

    try:
        result = execute_select(sql_query)
    except ValueError:
        return {"error": 'have no users;('}
    return result


def delete_by_id(id):
    sql_query = f'''
    DELETE FROM public."Users"
    WHERE id = {id}
    RETURNING id;
    '''

    try:
        result = execute_delete(sql_query)
    except ValueError as e:
        return {"error": str(e)}
    return {f"user{result['id']}": "is deleted"}
