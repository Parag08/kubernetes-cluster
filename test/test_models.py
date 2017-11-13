__author__ = '583153'


from cluster_management.src.models import User, Resource
from cluster_management.core import db

import unittest
import datetime
import time

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db.create_all()

class TestUserClass(unittest.TestCase):
    def test_intialisation_DB(self):
        ts = time.time()
        testuser = User(username='testuserunittesting1', email='email1@me.com', name='testuserunittesting',
                                     password='12345',
                                     timeStamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(testuser)
        db.session.commit()
        user = User.query.filter_by(username='testuserunittesting1').first()
        self.assertEqual('testuserunittesting1', user.username)
        self.assertEqual('email1@me.com', user.email)
        self.assertEqual('testuserunittesting', user.name)
        self.assertEqual('12345', user.password)
        db.session.delete(testuser)
        db.session.commit()
    def test_User(self):
        ts = time.time()
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        testuser = User(username='testuserunittesting', email='email@me.com', name='testuserunittesting',
                                     password='12345', timeStamp=timeStamp)
        resultjson = testuser.obj_dict()
        expectedjson = {'username': 'testuserunittesting', 'email': 'email@me.com', 'name': 'testuserunittesting','password': '12345', 'timeStamp': timeStamp}
        self.assertEqual(sorted(resultjson.items()),sorted(expectedjson.items()))
    def test_validate(self):
        ts = time.time()
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(User.validate(
            {'username': 'testuserunittesting', 'email': 'email@me.com', 'name': 'testuserunittesting',
             'password': '12345', 'timeStamp': timeStamp})["success"],True)
    def test_encode_auth_token(self):
        ts = time.time()
        user = User(
            email='test@test.com',
            password='test',
            username = 'test',
            name = 'test test',
            timeStamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        db.session.delete(user)
        db.session.commit()
    def test_decode_auth_token(self):
        ts = time.time()
        user = User(
            email='test@test.com',
            password='test',
            username = 'test',
            name = 'test test',
            timeStamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == 1)
        db.session.delete(user)
        db.session.commit()

class TestResourceManager(unittest.TestCase):
    def test_intialisation(self):
        ts = time.time()
        user = User(username='testuserunittesting2', email='email2@me.com', name='testuserunittesting',
                                     password='12345',
                                     timeStamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(username='testuserunittesting2').first()
        testresource = Resource(
            {'name': 'testresourceunittesting', 'hostType': 'aws', 'authType': 'jwt', 'userName': 'userName',
             'password': 'password', 'publicIP': 'publicIP', 'privateIP': 'privateIP', 'network': 'network',
             'keys': 'keys', 'rack': 'rack', 'geograph': 'geograph', 'CPU': 'CPU', 'RAM': 'RAM', 'Disk': 'Disk',
             'timeStamp': datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'),"user_id":user.id})
        db.session.add(testresource)
        db.session.commit()
        resource = Resource.query.filter_by(name='testresourceunittesting').first()
        self.assertEqual('testresourceunittesting', resource.name)
        self.assertEqual('aws', resource.hostType)
        self.assertEqual('jwt', resource.authType)
        self.assertEqual('userName', resource.userName)
        self.assertEqual('password', resource.password)
        self.assertEqual('publicIP', resource.publicIP)
        self.assertEqual('privateIP', resource.privateIP)
        self.assertEqual('network', resource.network)
        self.assertEqual('rack', resource.rack)
        self.assertEqual('geograph', resource.geograph)
        self.assertEqual('CPU', resource.CPU)
        self.assertEqual('RAM', resource.RAM)
        self.assertEqual('Disk', resource.Disk)
        self.assertEqual(user.id,resource.user_id)
        db.session.delete(resource)
        db.session.delete(user)
        db.session.commit()

if __name__ == '__main__':
    unittest.main()