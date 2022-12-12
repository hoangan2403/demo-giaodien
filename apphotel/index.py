from flask import render_template, request
from apphotel import app
import utils


@app.route("/")
def home():
    typeroom = utils.load_typeroom()
    roo = utils.load_room()
    kw = request.args.get("keyword")
    return render_template('index.html',
                           Room=roo,
                           TypeRoom=typeroom,
                           kw=kw)

@app.route("/list_room")
def list_rom():
    TypeRoom_id = request.args.get("TypeRoom_id")
    roo = utils.load_room(TypeRoom_id=TypeRoom_id)
    typeRoom = utils.load_typeroom()

    return render_template('danhsachphong.html',
                           Room=roo,
                           TypeRoom=typeRoom)

@app.route("/list_room2")
def list_rom2():
    TypeRoom_id = request.args.get("TypeRoom_id")
    roo = utils.load_room(TypeRoom_id=TypeRoom_id)
    typeRoom = utils.load_typeroom()

    return render_template('danhsachphong.html',
                           Room=roo,
                           TypeRoom=typeRoom)


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


@app.route("/signup", methods=['get', 'post'])
def account_signup():
    return render_template('signin.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')


if __name__ == '__main__':
    from apphotel.admin import *

    app.run(debug=True)