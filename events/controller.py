from fastapi import FastAPI


from entity import event as evt

from services import event_service
app = FastAPI()


@app.post("/event/create")
def create(event: evt.Event):
    return event_service.create(event)


@app.post("/event/update")
def update(event: evt.Event):
    return event_service.update(event)



@app.get("/event/get_by_id")
def get_by_id(id: int):
    return event_service.get_by_id(id)


@app.get("/event/get_all")
def get_all():
    return event_service.get_all()


@app.delete("/event/delete_by_id")
def delete_by_id(id: int):
    return event_service.delete_by_id(id)
