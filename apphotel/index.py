from flask import render_template, request, redirect, url_for
from flask_login import login_user, current_user, logout_user
from apphotel import app, login
from apphotel.decorators import anonymous_user
import utils
from apphotel.models import UserRole


@app.route("/")
def home():
    TypeRoom_id = request.args.get("TypeRoom_id")
    typeroom = utils.load_typeroom()
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    roo = utils.load_room(TypeRoom_id=TypeRoom_id, kw=kw, from_price=from_price, to_price=to_price)
    return render_template('Trangchu.html',
                           Room=roo,
                           TypeRoom=typeroom,
                           kw=kw,
                           from_price=from_price,
                           to_price=to_price)

@app.route("/list_room")
def list_room():
    TypeRoom_id = request.args.get("TypeRoom_id")
    roo = utils.load_room(TypeRoom_id=TypeRoom_id)
    typeRoom = utils.load_typeroom()
    Type_id = utils.get_typeroom_by_id(TypeRoom_id)
    return render_template('danhsachphong.html',
                           Room=roo,
                           TypeRoom=typeRoom,
                           Type_id=Type_id)

@app.route("/list_room")
def list_room2():
    TypeRoom_id = request.args.get("TypeRoom_id")
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    roo = utils.load_room(TypeRoom_id=TypeRoom_id, kw=kw, from_price=from_price, to_price=to_price)
    typeroom = utils.load_typeroom()

    return render_template('danhsachphong2.html',
                           Room=roo,
                           TypeRoom=typeroom,
                           kw=kw,
                           to_price=to_price,
                           from_price=from_price)


@app.route("/list-room-recep")
def list_room_recep():
    TypeRoom = utils.load_typeroom()
    Room = utils.load_room()
    return render_template('ListRoomRecep.html',TypeRoom=TypeRoom, Room=Room, user=current_user)


@app.route("/book-room/<int:room_id>")
def book_room(room_id):
    roo = utils.get_room_by_id(room_id)
    return render_template('BookingForm.html', Room=roo)


@app.route("/book-room//export/<int:room_id>")
def export_booking_form(room_id):
    err_msg = ''
    if request.method.__eq__('POST'):
        name_1 = request.form['name1']
        citizen_id = request.form['citizen_id']
        address = request.form['address']
        country = request.form['country']
        check_in_day = request.form['check_in_day']
        check_out_day = request.form['check_out_day']
        room = utils.check_room(room_id)
        if room:
            succes_msg = 'Đặt phòng thành công'
            return check_in_day
            # utils.BooKing(name_1=name_1, typecustomer_1=country, citizen_id_1=citizen_id,
            #                      address_1=address, room_id=room_id, check_in_day=check_in_day,
            #                      check_out_day=check_out_day)

            # return render_template('ExportBookingForm.html', succes_msg=succes_msg)
        else:
            err_msg = 'Phòng đã có khách đặt !!!'
    return render_template('BookingForm.html', err_msg=err_msg)


@app.route("/phieuthue")
def phieuthue_list():
    typeRoom = utils.load_typeroom()
    roo = utils.load_room()
    return render_template('Phieuthue.html',
                           Room=roo,
                           TypeRoom=typeRoom)


@app.route("/Room/<int:room_id>")
def categories_detail(room_id):
    roo = utils.get_room_by_id(room_id)
    return render_template('Chitietphong.html', Room=roo)


# @app.route("/listroom")
# def list_room_recep():
#     TypeRoom = utils.load_typeroom()
#     Room = utils.load_room()
#     return render_template('ListRoomRecep.html', TypeRoom=TypeRoom, Room=Room)


# @app.route("/recep-login", methods=['get', 'post'])
# def recep_signin():
#     err_msg = ''
#     if request.method.__eq__('POST'):
#         TypeRoom_id = request.args.get("TypeRoom_id")
#         typeroom = utils.load_typeroom()
#         kw = request.args.get("keyword")
#         from_price = request.args.get("from_price")
#         to_price = request.args.get("to_price")
#         roo = utils.load_room(TypeRoom_id=TypeRoom_id, kw=kw, from_price=from_price, to_price=to_price)
#         username = request.form.get('username')
#         password = request.form.get('password')
#         check = utils.check_login(user_name=username, password=password)
#         if check:
#             err_msg = 'Chào mừng đến với trang Lễ Tân '
#             return render_template('ListRoomRecep.html',
#                                    check=check,
#                                    err_msg=err_msg,
#                                    Room=roo,
#                                    TypeRoom=typeroom,
#                                    kw=kw,
#                                    to_price=to_price,
#                                    from_price=from_price
#                                    )
#         else:
#             err_msg = 'Tài khoản hoặc mật khẩu không chính xác !!!'
#
#     return render_template('signin.html', err_msg=err_msg)


@app.route("/recep-login", methods=['get', 'post'])
@anonymous_user
def recep_login():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = utils.check_login(username=username,
                                 password=password)
        if user:
            err_msg = 'Chào mừng đến với trang Lễ Tân'
            login_user(user=user)
            return render_template('Trangchu.html', err_msg=err_msg, user=user)
        else:
            err_msg = 'Tài khoản hoặc mật khẩu không chính xác !!!'
    return render_template('signin.html', err_msg=err_msg)

@app.route('/log_out_user')
def logout_my_user():
    logout_user()
    return render_template('signin.html')


# class RecepAuthenticatedModelView():
#     def is_accessible(self):
#         return current_user.is_authenticated and current_user.user_role.__eq__(UserRole.RECEP)
#
#
# class RecepAuthenticatedView():
#     def is_accessible(self):
#         return current_user.is_authenticated


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form[ 'username']
    password = request.form[ 'password']

    user = utils.check_login_admin(username=username,
                                   password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@login.user_loader
def load_user(user_id):
    return utils.get_user_by_id(user_id)


if __name__ == '__main__':
    from apphotel.admin import *

    app.run(debug=True)