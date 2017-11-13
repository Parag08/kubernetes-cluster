from flask import request, session, jsonify, make_response

from cluster_management import app
from cluster_management.core import db, InvalidUsage
from cluster_management.src.models import User, authorise, make_response_json

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import time
import datetime


def check_login(data):
    user = User.query.filter_by(username=data["username"]).first()
    if user is None:
        return {"error": "invalid username", "success": False}
    else:
        if data["password"] == user.password:
            return {"result": "valid user", "success": True, "data": user}
        else:
            return {"error": "password wrong", "success": False}


@app.route('/user/register', methods=['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        data = request.get_json(force=True)
        ts = time.time()
        data['timeStamp'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        if User.validate(data)["success"]:
            user = User(username=data["username"], email=data["email"], name=data["name"], timeStamp=data["timeStamp"],
                        password=data["password"])
            try:
                db.session.add(user)
                db.session.commit()
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as exp:
                make_response_json('fail',401,message="Registration failed (email or username already exist)")
        else:
            responseObject = {
                'status': 'fail',
                'message': User.validate(data)["error"],
            }
            return make_response(jsonify(responseObject)), 401
            # raise InvalidUsage(User.validate(data)["error"], status_code=410)
    else:
        return "registeration form..... :D"


@app.route('/user/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        data = request.get_json(force=True)
        result = check_login(data)
        if result["success"]:
            auth_token = result["data"].encode_auth_token(result["data"].id)
            if auth_token:
                session['logged_in'] = True
                session['user'] = result["data"].id
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
        else:
            raise InvalidUsage(result["error"], status_code=410)
    else:
        return "login page"


@app.route('/user/logout', methods=['GET'])
def user_logout():
    user_id, status, message = authorise(request)
    if status:
        return make_response_json('success', 200, message='Successfully logged out.')


@app.route('/user', methods=['GET'])
def user_listing():
    users = []
    for user in User.query.all():
        users.append(user.obj_dict())
    print(users)
    return jsonify(users)
