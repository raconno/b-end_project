from typing import Union
from pydantic import BaseModel
import logging


class User(BaseModel):
    id: Union[int, None] = None
    name: Union[str, None] = None
    last_name: Union[str, None] = None
    gender: Union[str, None] = None
    age: Union[int, None] = None
    city: Union[str, None] = None
    birth_day: Union[str, None] = None
    premium: Union[bool, None] = None
    ip: Union[str, None] = None
