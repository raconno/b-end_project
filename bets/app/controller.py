from fastapi import FastAPI
import json

from db_preparing import file_preparing as file

from app.entities import user as usr, bet as bt

from app.services import bet_service
from app.services import user_service
app = FastAPI()


@app.get("/")
def root():
    return json.dumps({"greeting": "welcome to ira`s lab!!"})


@app.on_event('startup')
def startup_event():
    file.start()


@app.post("/user/create")
def create(user: usr.User):
    return user_service.create(user)


@app.post("/bet/create")
def create(bet: bt.Bet):
    return bet_service.create(bet)


@app.post("/user/update")
def update(user: usr.User):
    return user_service.update(user)


@app.post("/bet/update")
def update(bet: bt.Bet):
    return bet_service.update(bet)


@app.get("/user/get_by_id")
def get_by_id(id: int):
    return user_service.get_by_id(id)


@app.get("/bet/get_by_id")
def get_by_id(id: int):
    return bet_service.get_by_id(id)


@app.get("/user/get_all")
def get_all():
    return user_service.get_all()


@app.get("/bet/get_all")
def get_all():
    return bet_service.get_all()


@app.delete("/user/delete_by_id")
def delete_by_id(id: int):
    return user_service.delete_by_id(id)


@app.delete("/bet/delete_by_id")
def delete_by_id(id: int):
    return bet_service.delete_by_id(id)
