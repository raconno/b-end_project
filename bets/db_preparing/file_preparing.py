from datetime import datetime
import random
import json
from app.services.executor import execute
from app.services.executor import execute_insert
from app.services.executor import execute_create

properties = {'name', 'last_name', 'time_created', 'gender', 'age', 'city', 'birth_day', 'premium', 'ip'}


class User:
    def _prepare_properties(self, dictionary):
        prepared_dictionary = {}
        for property in properties:
            value = dictionary.get(property)
            if property == 'age':
                # add age for the third lab
                prepared_dictionary[property] = random.randint(18, 50) if (value is None) else value
            elif property == 'time_created':
                prepared_dictionary[property] = f'\'{datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S")}\''
            elif value:
                prepared_dictionary[property] = f'\'{value}\''
            else:
                prepared_dictionary[property] = 'NULL'
        return prepared_dictionary

    def __init__(self, dictionary):
        prepared_dictionary = self._prepare_properties(dictionary)
        self.name = prepared_dictionary['name']
        self.last_name = prepared_dictionary['last_name']
        self.time_created = prepared_dictionary['time_created']
        self.gender = prepared_dictionary['gender']
        self.age = prepared_dictionary['age']
        self.city = prepared_dictionary['city']
        self.birth_day = prepared_dictionary['birth_day']
        self.premium = prepared_dictionary['premium']
        self.ip = prepared_dictionary['ip']

    def __members(self):
        return self.name, self.time_created

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__members() == other.__members()
        else:
            return False

    def __hash__(self):
        return hash(self.__members())

    def create_sql_query(self):
        sql_query = f'''
        INSERT INTO public."Users"(
            name, last_name, time_created, gender, age, city, birth_day, premium, ip)
            VALUES ({self.name}, {self.last_name}, {self.time_created}, {self.gender}, {self.age},
            {self.city}, {self.birth_day}, {self.premium}, {self.ip})
            RETURNING id;
        '''
        return sql_query


def create_tables():
    execute_create('''
    CREATE SEQUENCE "Users_id_seq";

    CREATE TABLE public."Users"
    (
        id integer NOT NULL DEFAULT nextval('"Users_id_seq"'::regclass),
        name text NOT NULL,
        last_name text,
        time_created timestamp without time zone NOT NULL,
        gender text,
        age smallint NOT NULL,
        city text,
        birth_day text,
        premium boolean,
        ip text,
        CONSTRAINT "Users_pkey" PRIMARY KEY (id)
    )''')

    execute_create('''
    CREATE SEQUENCE "Events_id_seq";

    CREATE TABLE public."Events"
    (
        id integer NOT NULL DEFAULT nextval('"Events_id_seq"'::regclass),
        type text NOT NULL,
        team_1 text NOT NULL,
        team_2 text NOT NULL,
        event_date date NOT NULL,
        score text NOT NULL,
        state text NOT NULL,
        CONSTRAINT "Events_pkey" PRIMARY KEY (id)
    )''')

    execute_create('''
    CREATE SEQUENCE "Bets_id_seq";

    CREATE TABLE public."Bets"
(
    id integer NOT NULL DEFAULT nextval('"Bets_id_seq"'::regclass),
    data_created date NOT NULL,
    user_id integer NOT NULL,
    event_id integer NOT NULL,
    market text NOT NULL,
    state text NOT NULL,
    CONSTRAINT "Bets_pkey" PRIMARY KEY (id),
    CONSTRAINT user_id_fkey FOREIGN KEY (user_id)
        REFERENCES public."Users" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT event_id_fkey FOREIGN KEY (event_id)
        REFERENCES public."Events" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)
    ''')


def start():
    check_if_exist = execute('''
    SELECT EXISTS (
    SELECT FROM
        pg_tables
    WHERE
        schemaname = 'public' AND
        tablename  = 'Events'
    );
    ''')

    if check_if_exist:
        return

    create_tables()

    file = open('db_preparing/data.jsonl', 'r', encoding='utf-8')
    users = set()
    for user_json in file:
        user_data = json.loads(user_json)
        user = User(user_data)
        users.add(user)
    file.close()

    for user in users:
        insert = user.create_sql_query()
        execute_insert(insert)
