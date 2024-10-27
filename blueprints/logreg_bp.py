from aifc import Error
from flask import Blueprint, jsonify, make_response, request, Response
from mysql_connection.mysql_db import mydb

# Створюємо блупрінт
logreg_bp = Blueprint('logreg', __name__)


@logreg_bp.route('/logreg/login', methods=["POST"])
def login():
    data = request.json
    cursor = mydb.cursor()
    query = f"select * from `Keys` where username = '{
        data["username"]}' and password = '{data["password"]}'"
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    if (user is None):
        return jsonify({"message": "Неправильний логін або пароль"}), 404
    resp = make_response(jsonify({"message": "Ви ввійшли в акаунт"}))
    resp.set_cookie('role', user[3])
    return resp, 200


@logreg_bp.route('/logreg/signup', methods=["POST"])
def signup():
    if request.cookies['role'] not in ['owner', 'admin']:
        return jsonify({"message": "Недостатньо прав"}), 400
    data = request.json
    if request.cookies['role'] != 'owner' and data['role'] == 'admin':
        return jsonify({"message": "Недостатньо прав"}), 400
    cursor = mydb.cursor()
    query = f"insert into `Keys` (username, password, role) values ('{
        data["username"]}','{data["password"]}','{data["role"]}')"
    try:
        cursor.execute(query)
        print("yes")
        mydb.commit()
        cursor.close()
        return jsonify({"message": "Ви успішно зареєстрували користувача"}), 200
    except Error as err:
        print(err)


@logreg_bp.route('/logreg/get-password', methods=["POST"])
def get_password():
    data = request.json["username"]
    cursor = mydb.cursor()
    query = f"select password from `Keys` where username = '{data}'"
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    if (user is None):
        return jsonify({"message": "Неправильний логін"}), 404
    return jsonify(user[0]), 200
