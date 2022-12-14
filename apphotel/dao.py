import hashlib
from apphotel import app, db
from apphotel.models import TypeRoom, Room, Account


def account_signup(name, username, password, user_role):
    password = str(hashlib.md5(password.strip().endcode('utf-8')).hexdigest())
    account = Account(name=name.strip(), user=username.strip(), password=password, user_role=user_role)

    db.session.add(account)
    db.session.commit()
