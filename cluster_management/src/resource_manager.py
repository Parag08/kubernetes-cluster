import time
import datetime

from flask import session, request, jsonify, abort, make_response
from cluster_management.src.models import Resource, User, authorise, make_response_json
from cluster_management import app
from cluster_management.core import db

import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route('/resources/<machine_id>', methods=['GET', 'PUT', 'DELETE'])
@app.route('/resources/', methods=['POST', 'GET'])
def resource(machine_id=None):
    user_id, status, message = authorise(request)
    if status:
        if machine_id is None:
            if "GET" == request.method:
                '''get all machines associated with user from the database and display it'''
                try:
                    resources_list = []
                    user = User.query.filter_by(id=user_id).first()
                    resources_of_user = user.resources.all()
                    for resource in resources_of_user:
                        resources_list.append(resource.obj_dict())
                    return make_response_json("success", 200, data=resources_list)
                except Exception as exp:
                    logger.error(exp, exc_info=True)
                    resources_list = []
                    return make_response_json("failed", 404, message=exp.message)
            else:
                '''add new machines to the database'''
                data = request.get_json(force=True)
                ts = time.time()
                data['timeStamp'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                data['user_id'] = user_id
                if Resource.validate(data)["success"]:
                    resource = Resource(data)
                    db.session.add(resource)
                    db.session.commit()
                    return "resource registered"
                else:
                    abort(410)
                    # raise InvalidUsage(Resource.validate(data)["error"], status_code=410)
        else:
            if "GET" == request.method:
                # TODO make this user safe (any user can access any machine if he has machine ID
                try:
                    resource = Resource.query.filter_by(id=machine_id).first()
                    if resource.user_id == user_id:
                        return jsonify(resource)
                    else:
                        abort(404)
                except Exception as exp:
                    logger.error(exp, exc_info=True)
                    abort(404)
            elif "PUT" == request.method:
                '''Editing already existing machine'''
                # TODO make this user safe (any user can access any machine if he has machine ID
                try:
                    data = request.get_json(force=True)
                    ts = time.time()
                    data['timeStamp'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    data['user_id'] = session['user']
                    resource = Resource.query.filter_by(id=machine_id).first()
                    if Resource.validate(data)["success"]:
                        resource = Resource(data)
                        db.session.update(resource)
                        db.session.commit()
                except Exception as exp:
                    logger.error(exp, exc_info=True)
                    abort(404)
            else:
                return "yet to be implemented"
    else:
        response_object = {
            'status': 'fail',
            'message': message
        }
        return make_response(jsonify(response_object)), 401