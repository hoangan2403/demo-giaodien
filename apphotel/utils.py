import hashlib
import json, os
from apphotel import app, db
from apphotel.models import TypeRoom, Room, Account, UserRole, Customer, BookingForm, ReceiptDetails, Receipt
from sqlalchemy import func

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


def get_typeroom_by_id(id):
    return TypeRoom.query.filter(TypeRoom.id.__eq__(id))


def get_room_by_id(room_id):
    roo = Room.query.all()
    for c in roo:
        if c.id == room_id:
            return c


def check_login(username, password, user_role=UserRole.RECEP):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return Account.query.filter(Account.username.__eq__(username.strip()),
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


def check_room(room_id):
    return Room.query.filter(Room.id==room_id, Room.active==0).first()


class BooKing:

    def booking_room_1(self, name_1, typecustomer_1, citizen_id_1, address_1, room_id, check_in_day, check_out_day):
        customer = Customer(Name=name_1, Country=typecustomer_1, Citizen_id=citizen_id_1, Address=address_1)
        booking_form = BookingForm(Room_id=room_id, Check_inDate=check_in_day, Check_outDay=check_out_day,
                                   Cus1=customer)
        db.session.add(customer)
        db.session.add(booking_form)
        db.session.commit()

    def booking_room_2(self, name_1, typecustomer_1, citizen_id_1, address_1,
                     name_2, typecustomer_2, citizen_id_2, address_2,
                     room_id, check_in_day, check_out_day):
        customer_1 = Customer(Name=name_1, Country=typecustomer_1, Citizen_id=citizen_id_1, Address=address_1)
        customer_2 = Customer(Name=name_2, Country=typecustomer_2, Citizen_id=citizen_id_2, Address=address_2)
        booking_form = BookingForm(Room_id=room_id, Check_inDate=check_in_day, Check_outDay=check_out_day,
                                   Cus1=customer_1, Cus2=customer_2)
        db.session.add(customer_1)
        db.session.add(customer_2)
        db.session.add(booking_form)
        db.session.commit()

    def booking_room_3(self, name_1,typecustomer_1, citizen_id_1, address_1,
                     name_2, typecustomer_2, citizen_id_2, address_2,
                     name_3, typecustomer_3, citizen_id_3, address_3,
                     room_id, check_in_day, check_out_day):
        customer_1 = Customer(Name=self, Country=typecustomer_1, Citizen_id=citizen_id_1, Address=address_1)
        customer_2 = Customer(Name=name_2, Country=typecustomer_2, Citizen_id=citizen_id_2, Address=address_2)
        customer_3 = Customer(Name=name_3, Country=typecustomer_3, Citizen_id=citizen_id_3, Address=address_3)
        booking_form = BookingForm(Room_id=room_id, Check_inDate=check_in_day, Check_outDay=check_out_day,
                                   Cus1=customer_1, Cus2=customer_2, Cus3=customer_3)
        db.session.add(customer_1)
        db.session.add(customer_2)
        db.session.add(customer_3)
        db.session.add(booking_form)
        db.session.commit()



def count_product_by_cate():
    return db.session.query(TypeRoom.id, TypeRoom.name, func.count(Room.id)) \
        .join(Room, Room.TypeRoom_id.__eq__(TypeRoom.id), isouter=True) \
        .group_by(TypeRoom.id).order_by(-TypeRoom.name).all()


def stats_revenue_by_prod(kw=None, from_date=None, to_date=None):
    query = db.session.query(Room.id, Room.name, func.sum(ReceiptDetails.quantity * ReceiptDetails.price)) \
        .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Room.id)) \
        .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id))

    if kw:
        query = query.filter(Room.name.contains(kw))

    if from_date:
        query = query.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        query = query.filter(Receipt.created_date.__le__(to_date))

    return query.group_by(Room.id).all()