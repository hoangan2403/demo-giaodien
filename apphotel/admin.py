import flask_admin
from apphotel import admin, db
from apphotel.models import TypeRoom,Room
from flask_admin.contrib.sqla import ModelView

admin.add_view(ModelView(TypeRoom, db.session, name='Loại phòng'))
admin.add_view(ModelView(Room, db.session, name='Quản lý phòng'))