from apphotel import db, app, utils, dao
from flask_admin import Admin, BaseView, expose
from apphotel.models import TypeRoom, Room, Account
from flask_admin.contrib.sqla import ModelView
from flask import request, render_template, redirect, url_for

admin = Admin(app=app, name="Quản trị khách sạn", template_mode='bootstrap4')
app.secret_key = '#@!$%^#$^$#!@%$@#$^%*&^%dsad!2321321r%^%$&^%Sfdfds'


class ListRoomView(ModelView):
    can_view_details = True
    can_export = True
    can_edit = True
    column_display_pk = True
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'create_date']
    column_sortable_list = ['name', 'price']


class ListAccount(ModelView):
    can_create = False
    can_edit = False
    column_searchable_list = ['name', 'username']
    column_exclude_list = ['password']
    column_sortable_list = ['name']


class SignUpView(BaseView):
    @expose('/')
    def SignUp(self):
        return self.render('admin/signup.html')


class AccountSignupView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def account_signup(self):
        err_msg = ""
        succes_msg = ""
        if request.method.__eq__('POST'):
            user_role = request.form.get('value')
            name = request.form.get('name')
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
        try:
            if password.strip().__eq__(confirm_password.strip()):
                succes_msg = 'Tạo tài khoản thành công !'
                utils.account_signup(name=name,
                                     username=username,
                                     password=password,
                                     user_role=user_role)
                return succes_msg

                return self.render('admin/signup.html', succes_msg=succes_msg)
            else:
                err_msg = 'Mật khẩu không khớp'
        except Exception as ex:
            print(str(ex))
            err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        return self.render('admin/signup.html', err_msg=err_msg)


# @app.route('/', methods=['GET', 'POST'])
# def account_signup():
#     err_msg = ""
#     succes_msg = ""
#     if request.method.__eq__('POST'):
#         user_role = request.form.get('value')
#         name = request.form.get('name')
#         username = request.form.get('username')
#         password = request.form.get('password')
#         confirm_password = request.form.get('confirm_password')
#     try:
#         if password.strip().__eq__(confirm_password.strip()):
#             succes_msg = 'Tạo tài khoản thành công !'
#             utils.account_signup(name=name,
#                                  username=username,
#                                  password=password,
#                                  user_role=user_role)
#             return succes_msg
#
#             # return self.render('./admin/signup.html', succes_msg=succes_msg)
#         else:
#             err_msg = 'Mật khẩu không khớp'
#     except Exception as ex:
#         print(str(ex))
#         err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
#     # return err_msg
#     return render_template('admin/signup.html', err_msg=err_msg)


admin.add_view(ModelView(TypeRoom, db.session, name='Loại phòng'))
admin.add_view(ListRoomView(Room, db.session, name='Quản lý phòng'))
admin.add_view(ListAccount(Account, db.session, name="Quản lý tài khoản"))
admin.add_view(SignUpView(name='Đăng ký tài khoản', endpoint='signup'))
