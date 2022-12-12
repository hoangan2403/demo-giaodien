from apphotel import db, app
from flask_admin import Admin
from apphotel.models import TypeRoom, Room
from flask_admin.contrib.sqla import ModelView

admin = Admin(app=app, name="Quản trị khách sạn", template_mode='bootstrap4')
app.secret_key='#@!$%^#$^$#!@%$@#$^%*&^%dsad!2321321r%^%$&^%Sfdfds'

class ListRoomView(ModelView):
    can_view_details = True
    can_export = True
    can_edit = True
    column_display_pk = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'create_date']
    column_sortable_list = ['name', 'price']



admin.add_view(ModelView(TypeRoom, db.session, name='Loại phòng'))
admin.add_view(ListRoomView(Room, db.session, name='Quản lý phòng'))
