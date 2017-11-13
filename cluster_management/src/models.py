__author__ = '583153'

from cluster_management.core import db
from cluster_management import app

from flask import make_response, jsonify

from jsonschema import validate

import datetime
import jwt
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    timeStamp = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    resources = db.relationship('Resource', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

    def obj_dict(self):
        dict_to_return = self.__dict__
        del dict_to_return['_sa_instance_state']
        return dict_to_return

    @staticmethod
    def validate(json):
        schema = {"type": "object", "properties": {"username": {"type": "string"}, "email": {"type": "string"},
                                                   "name": {"type": "string"}, "timeStamp": {"type": "string"},
                                                   "password": {"type": "string"}},
                  "required": ["username", "email", "name", "timeStamp", "password"]}
        try:
            validate(json, schema)
            return {"success": True}
        except TypeError as err:
            return {"success": False, "error": str(err)}

    def encode_auth_token(self, user_id):
        """
        generate the Auth Token
        :param user_id:
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=600),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload,
                              app.config.get('SECRET_KEY'),
                              algorithm='HS256'
            )
        except Exception as exp:
            logger.error(exp, exc_info=True)

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    hostType = db.Column(db.String(120), unique=False, nullable=True)
    authType = db.Column(db.String(120), unique=False, nullable=False)
    userName = db.Column(db.String(120), unique=False, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=True)
    publicIP = db.Column(db.String(120), unique=False, nullable=False)
    privateIP = db.Column(db.String(120), unique=False, nullable=False)
    network = db.Column(db.String(120), unique=False, nullable=True)
    keys = db.Column(db.String(120), unique=False, nullable=True)
    rack = db.Column(db.String(120), unique=False, nullable=True)
    geograph = db.Column(db.String(120), unique=False, nullable=True)
    CPU = db.Column(db.String(120), unique=False, nullable=True)
    RAM = db.Column(db.String(120), unique=False, nullable=True)
    Disk = db.Column(db.String(120), unique=False, nullable=True)
    timeStamp = db.Column(db.String(120), unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    list_variables = ["keys", "password", "CPU", "network", "userName", "authType", "name", "timeStamp", "RAM",
                      "geograph", "hostType", "privateIP", "publicIP", "Disk", "rack", "user_id"]

    @property
    def __repr__(self):
        return u'<User {0!r:s}>'.format(self.name)

    def __init__(self, data):
        for variable in self.list_variables:
            try:
                setattr(self, variable, data[variable])
            except Exception as exp:
                logger.error(exp, exc_info=True)

    def obj_dict(self):
        dict_to_return = self.__dict__
        del dict_to_return['_sa_instance_state']
        return dict_to_return

    @staticmethod
    def validate(json):
        """

        :rtype : object
        """
        schema = {'type': "object", 'properties': {"name": {"type": "string"}, "hostType": {"type": "string"},
                                                   "authType": {"type": "string"}, "timeStamp": {"type": "string"},
                                                   "userName": {"type": "string"}, "password": {"type": "string"},
                                                   "publicIP": {"type": "string"}, "privateIP": {"type": "string"},
                                                   "network": {"type": "string"}, "keys": {"type": "string"},
                                                   "rack": {"type": "string"}, "geograph": {"type": "string"},
                                                   "CPU": {"type": "string"}, "RAM": {"type": "string"},
                                                   "Disk": {"type": "string"}, "user_id": {"type": "number"}},
                  'additionalProperties': False}
        try:
            validate(json, schema)
            return {"success": True}
        except ValueError as err:
            return dict(success=False, error=err)


def make_response_json(status, response_code, message=None, error=None, data=None):
    """
    :param status: (string) status of request
    :param response_code: (integer) response code
    :param message: (string) any message to be delivered in response
    :param error: (string) any error message
    :param data: (list or json object) list of return data value
    :return: response | code
    """
    response_object = dict(
        status=status,
        data=data,
        message=message,
        error=error
    )
    for key, value in list(response_object.items()):
        if value is None:
            del response_object[key]

    return make_response(jsonify(response_object)), response_code


def authorise(request, asset_name=None, asset_id=None):
    """
    :param request:
    :return Boolean, user_id , message:
    """
    if asset_name is None and asset_id is None:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                return resp, True, None
            else:
                return -1, False, resp
        else:
            return -1, False, 'Provide a valid auth token.'