import unittest

import os
import json
from smapi import create_app
from config import Config
from flask_jwt_extended import JWTManager, create_access_token
from smapi.models.dbase import Databasehandler
# from tests import BaseTestCase
db=Databasehandler()
class SalesTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(mode='testing')
        self.test_client= self.app.test_client()
        self.db=db
        self.token=''
        self.sale_data={
            "saleId":1,
            "product_id":"3",
            "entered_by":"attendant",
            "quantity":4,           
        }
        self.badsaledata={
            "saleId":1,
            "product_id":"3",
            "entered_by":"attendant",
            "quantity":0, 
        }

        
    def test_add_sale_order(self):
        
        with self.app.app_context():
            token = create_access_token('false')
            headers = {'Authorization': f'Bearer {token}'}
            response = self.test_client.post(
                '/api/v2/sales',
                headers=headers,
                content_type='application/json',
                data=self.sale_data
            )
            return(response.status)
        
    def test_fetch_single_sale_order(self):

        with self.app.app_context():
            token = create_access_token('false')
            headers = {'Authorization': f'Bearer {token}'}
            response = self.test_client.get(
                '/api/v2/sales/1',
                headers=headers,
                content_type='application/json',
                data= self.sale_data
            )
            return(response.status)

    def test_fetch_all_sale_orders(self):
        with self.app.app_context():
            token = create_access_token('true')
            headers = {'Authorization': f'Bearer {token}'}
            response = self.test_client.get(
                '/api/v2/sales',
                headers=headers,
                content_type='application/json'
            )
        return(response.status)

    def test_add_sale_with_wrong_data_types(self):
        with self.app.app_context():
            token = create_access_token('false')
            headers = {'Authorization': f'Bearer {token}'}
            response = self.test_client.post(
                '/api/v2/sales',
                headers=headers,
                content_type='application/json',
                data=self.badsaledata
            )
            return(response.status)
        # self.assertIn("",str(response.data))

    # def tearDown(self):
    #     db.drop_table('sales')