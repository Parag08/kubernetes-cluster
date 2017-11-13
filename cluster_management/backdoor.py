__author__ = '583153'

BACK_DOOR_TOKEN = 'qazwsxedc'

""" Highly contagious please delete before deployment"""

from cluster_management.src.models import User, Resource
from cluster_management import app

from flask import jsonify


@app.route('/backdoor/resources/<token>', methods=["GET"])
def backdoor_resources(token):
    if token == BACK_DOOR_TOKEN:
        resources_list = []
        for resource in Resource.query.all():
            resources_list.append(resource.obj_dict())
        return jsonify(resources_list)
