import unittest

import os
import json
from smapi import create_app
from config import Config
from flask_jwt_extended import JWTManager, create_access_token
from smapi.models.dbase import Databasehandler
# from tests import BaseTestCase
db=Databasehandler()

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(mode='testing')
        self.test_client= self.app.test_client()
        self.db=db
        self.token=''
        self.auth_data = {
            'username': 'admin',
            'password': 'admin',
            'role': 'true'
        }
        self.auth_data2 = {
            'username': 'test_attendant',
            'password': 'saxsa',
            'role':'false'
        }
        self.invalid_data={
            'username': 'clarice',
            'password': 'admin',
            'role': 'true'
        }
        self.invalid_data2={
            'username': 'admin',
            'password': 'password',
            'role': 'true'
        }


    def test_index(self):
        response= self.test_client.get('/', content_type='application/json')
        self.assertEqual(response.status_code,200)
        self.assertIn("StoreManager auth. Manage your Products and Sales efficiently using DBMS'",str(response.data))

    def test_admin_login(self):

        response = self.test_client.post('/api/v2/auth/login',
                                    data=json.dumps(self.auth_data),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertIn("admin, successfully logged in",  str(response.data))
    
    def test_attendant_login(self):
        response = self.test_client.post('/api/v2/auth/login',
                                    data=json.dumps(self.auth_data2),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid credentials", str(response.data))

    def test_wrong_username(self):
        response = self.test_client.post('/api/v2/auth/login',
                                    data=json.dumps(self.invalid_data),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid credentials",  str(response.data))

    def test_wrong_password(self):
        response = self.test_client.post('/api/v2/auth/login',
                                    data=json.dumps(self.invalid_data2),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid credentials",  str(response.data))
    
    def test_login_with_no_values(self):
        data={
            'username': "",
            'password': 'admin',
            'role': 'false'
        }

        response = self.test_client.post('/api/v2/auth/login',
                                    data=json.dumps(data),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username is missing",  str(response.data))
    def test_no_password_login(self):
        data2={
            'username': "admin",
            'password': '',
            'role': 'false'
        }

        response = self.test_client.post('/api/v2/auth/login',
                                    data=json.dumps(data2),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password is missing",  str(response.data))
    def test_signup_as_attendant(self):
        sdata=("charly","password")
        response = self.test_client.post('/api/v2/auth/signup',
                                    data=json.dumps(sdata),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, 401)
        self.assertIn("Missing Authorization Header",  str(response.data))
    def test_signup_as_admin(self):
        sdata={
            "username":"charly",
            "password":"password",
            "role":"false"
        }
        with self.app.app_context():
            token = create_access_token('true')
            headers={'Authorization':f'Bearer {token}'}

            response = self.test_client.post(
                '/api/v2/auth/signup',
                headers=headers,
                data=json.dumps(sdata),
                content_type='application/json')
            return(response.status)

    def tearDown(self):
        self.db.drop_table('users')
             