from enum import Enum
from typing import Union
from pydantic import BaseModel

class StateEnum(str, Enum):
    created = 'created'
    active = 'active'
    finished = 'finished'

class Event(BaseModel):
    id: Union[int, None] = None
    type: Union[str, None] = None
    team_1: Union[str, None] = None
    team_2: Union[str, None] = None
    event_date: Union[str, None] = None
    score: Union[str, None] = None
    state: Union[StateEnum, None] = None
