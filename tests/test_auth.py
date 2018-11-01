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
            'password': 'admin'
        }
        self.auth_data2 = {
            'username': 'test_attendant',
            'password': 'saxsa'
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

        db.add_user('test_attendant','saxsa')        
        response = self.test_client.post('/api/v2/auth/login',
                                    data=json.dumps(self.auth_data2),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("test_attendant, successfully logged in", str(response.data))

   