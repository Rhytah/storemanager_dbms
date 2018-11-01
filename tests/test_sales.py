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
            "product_name":"Foam",
            "unit_price":5000,
            "quantity":4,
            "entered_by":"attendant"
            
        }
        
    def test_add_sale_order(self):
        db.add_sale("attendant","foam","5000","4")
        with self.app.app_context():
            token = create_access_token('attendant')
            headers = {'Authorization': f'Bearer {token}'}
            response = self.test_client.post(
                '/api/v2/sales',
                headers=headers,
                content_type='application/json',
                data=self.sale_data
            )
            return(response.status)
        
    def test_fetch_single_sale_order(self):
        db.add_sale("attendant","foam","5000","4")
        res=db.get_a_sale(1)
        self.assertEqual("('attendant', 'foam', 5000, 4)",str(res))
        with self.app.app_context():
            token = create_access_token('attendant')
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
            token = create_access_token('admin')
            headers = {'Authorization': f'Bearer {token}'}
            response = self.test_client.get(
                '/api/v2/sales',
                headers=headers,
                content_type='application/json'
            )
        return(response.status)

    # def tearDown(self):
    #     db.drop_table('sales')