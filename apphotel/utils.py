import hashlib
import json, os
from apphotel import app, db
from apphotel.models import TypeRoom, Room, Account, User, UserRole


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_room(TypeRoom_id=None, kw=None, to_price=None, from_price=None):
    roo = Room.query.all()
    if TypeRoom_id:
        roo = Room.query.filter(Room.TypeRoom_id.__eq__(TypeRoom_id))
    if kw:
        roo = Room.query.filter(Room.description.contains(kw))
    if from_price:
        roo = Room.query.filter(Room.price.__ge__(from_price))
    if to_price:
        roo = Room.query.filter(Room.price.__le__(to_price))

    return roo


def load_typeroom():
    return TypeRoom.query.all()


def get_room_by_id(room_id):
    roo = Room.query.all()
    for c in roo:
        if c.id == room_id:
            return c


def check_login(user_name, password, user_role=UserRole.RECEP):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Account.query.filter(Account.username.__eq__(user_name.strip()),
                                Account.password.__eq__(password),
                                Account.user_role.__eq__(user_role)).first()


def check_login_admin(username, password, user_role=UserRole.ADMIN):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Account.query.filter(Account.username.__eq__(username.strip()),
                                Account.password.__eq__(password),
                                Account.user_role.__eq__(user_role)).first()


def get_user_by_id(user_id):
    return Account.query.get(user_id)


def account_signup(name, username, password, user_role):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    account = Account(name=name.strip(), username=username.strip(), password=password, user_role=user_role)

    db.session.add(account)
    db.session.commit()
