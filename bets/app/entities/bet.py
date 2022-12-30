from enum import Enum
from typing import Union
from pydantic import BaseModel

class MarketEnum(str, Enum):
    team_1 = 'team_1'
    team_2 = 'team_2'
    draw = 'draw'

class Bet(BaseModel):
    id: Union[int, None] = None
    user_id: Union[int, None] = None
    event_id: Union[int, None] = None
    market: Union[MarketEnum, None] = None
