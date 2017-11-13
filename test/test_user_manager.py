from cluster_management import app
from cluster_management.core import db

import unittest
import json
import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class TestUserManager(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tmp/testdatabase.db'
        app.testing = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def test_user_registration(self):
        response = self.app.post(
            '/user/register',
            data=json.dumps(dict(
                email='test@email.com',
                password='test',
                username='test',
                name='test test'
            )),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_user_login(self):
        response = self.app.post(
            '/user/register',
            data=json.dumps(dict(
                email='test1@email.com',
                password='test1',
                username='test1',
                name='test test'
            )),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)
        response = self.app.post(
            '/user/login',
            data=json.dumps(dict(
                username='test1',
                password='test1'
            ))
        )
        data = json.loads(response.data.decode())
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Successfully logged in.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        response = self.app.post(
            '/user/register',
            data=json.dumps(dict(
                email='test2@email.com',
                password='test2',
                username='test2',
                name='test test2'
            )),
            content_type='application/json')
        data = json.loads(response.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully registered.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertEqual(response.status_code, 201)
        response_login = self.app.post(
            '/user/login',
            data=json.dumps(dict(
                username='test2',
                password='test2'
            ))
        )
        data = json.loads(response_login.data.decode())
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['message'], 'Successfully logged in.')
        self.assertTrue(data['auth_token'])
        self.assertTrue(response_login.content_type == 'application/json')
        self.assertEqual(response_login.status_code, 200)
        auth_token = data['auth_token']
        print(auth_token,type(auth_token))
        response_logout = self.app.post(
            '/user/logout',
            headers=json.dumps(dict(
                Authorization='Bearer ' + auth_token
            ))
        )
        data = json.loads(response_logout.data.decode())
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(data['message'] == 'Successfully logged out.')
        self.assertEqual(response_logout.status_code, 200)

    def tearDown(self):
        # windows
        path_to_tmp_db = APP_ROOT[:-4] + 'cluster_management\\tmp\\testdatabase.db'
        # linux
        # path_to_tmp_db = APP_ROOT[:-4] +  '/cluster_management/tmp/testdatabase.db
        os.remove(path_to_tmp_db)


if __name__ == '__main__':
    unittest.main()
