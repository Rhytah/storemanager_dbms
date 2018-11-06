import unittest

import os
import json
from smapi import create_app
from config import Config
from flask_jwt_extended import JWTManager, create_access_token
from smapi.models.dbase import Databasehandler
# from tests import BaseTestCase
# db=Databasehandler()


class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(mode='testing')
        self.test_client= self.app.test_client()
        self.db=Databasehandler()
        
        self.samplepdt={
            "product_id":1,
            "product_name":"crocs",
            "unit_price": "3000"
        }

        self.token=''
        self.auth_data = {
            'username': 'admin',
            'password': 'admin'
        }
        

        self.request_data={
            "productId":1,
            "product_name":"Foam",
            "unit_price":3000
        }
        self.wrong_productdata={
            "product_id":1,
            "product_name":" ",
            "unit_price":"3000"
        }
        
    def test_add_product(self):
        # db.add_pdt("cupps",30000)
        res=self.test_client.post('/api/v2/products', data=json.dumps(self.request_data),
        content_type='application/json')
        self.assertEqual(res.status_code,401)
        self.assertIn('Missing Authorization Header', str(res.data))

    
    def test_admin_can_add_product(self): 
        with self.app.app_context():
            token = create_access_token('true')
            headers={'Authorization':f'Bearer {token}'}

            response = self.test_client.post(
                '/api/v2/products',
                headers=headers,
                content_type='application/json')
            return(response.status)


    def test_add_product_with_wrong_data(self):
        with self.app.app_context():
            token = create_access_token('true')
            headers={'Authorization':f'Bearer {token}'}
            response = self.test_client.post(
            '/api/v2/products',headers=headers,
            content_type='application/json',
            data = self.wrong_productdata)
            self.assertEqual(response.status_code,400)

    def test_add_product_without_token(self):
        response = self.test_client.post(
            '/api/v2/products', data=json.dumps(self.request_data), content_type='application/json'
        )
        self.assertEqual(response.status_code,401)
        self.assertIn(
            'Missing Authorization Header', str(response.data)
        )
    def test_add_product_as_attendant(self):
        with self.app.app_context():
            token = create_access_token('false')
            headers = {'Authorization': f'Bearer {token}'}
            response = self.test_client.post(
                '/api/v2/product',
                headers=headers,
                content_type='application/json'
            )
            return(response.status)
       
    
    def test_fetch_products(self):
        response = self.test_client.get( 
            '/api/v2/products', data=json.dumps(self.request_data), content_type = 'application/json')
        self.assertEqual(response.status_code,404)
        

    def test_fetch_single_product(self):    
        response = self.test_client.get('/api/v2/products/1',
                            content_type='application/json',
                            data=json.dumps(self.samplepdt)
                            )      
        self.assertEqual(response.status_code,200)

    def test_remove_pdt(self):
        with self.app.app_context():
            token = create_access_token('true')
            headers = {'Authorization': f'Bearer {token}'}
            response = self.test_client.delete(
                '/api/v2/product/1',
                headers=headers,
                content_type='application/json',
                data=self.request_data
            )
            return(response.status)

    def test_modify_pdt(self):
        with self.app.app_context():
            token = create_access_token('true')
            headers = {'Authorization': f'Bearer {token}'}
            response = self.test_client.put(
                '/api/v2/product/1',
                headers=headers,
                content_type='application/json'
            )
            return(response.status)

    def test_add_a_product_without_name(self):
        with self.app.app_context():
            token = create_access_token('true')
            headers={'Authorization':f'Bearer {token}'}
            response = self.test_client.post('/api/v2/products',
            headers=headers,
            data=json.dumps({"product_id": 2 , "product_name": " ", "unit_price":5000, "stock":30}),
            content_type='application/json')
            self.assertEqual(response.status_code,400)
            self.assertTrue("product name is missing",str(response.data))
    
    def test_add_a_product_without_price(self):
        with self.app.app_context():
            token = create_access_token('true')
            headers={'Authorization':f'Bearer {token}'}
            response = self.test_client.post('/api/v2/products',
            headers=headers,
            data=json.dumps({"product_id": 2 , "product_name": "Gloves ", "stock":30}),
            content_type='application/json')
            self.assertEqual(response.status_code,400)
            self.assertTrue("unit_price is missing",str(response.data))
            
    def tearDown(self):
        self.db.drop_table('products')
    
       
    

