import json, os
from apphotel import app
from apphotel.models import TypeRoom, Room


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_room(TypeRoom_id=None, kw=None):

    roo = Room.query.all()
    if TypeRoom_id:
        roo = Room.query.filter(Room.TypeRoom_id.__eq__(TypeRoom_id))
    if kw:
        roo = Room.query.filter(Room.name.contains(kw))
    return roo


def load_typeroom():
    return TypeRoom.query.all()


def get_room_by_id(room_id):
    roo = Room.query.all()
    for c in roo:
        if c.id == room_id:
            return c
