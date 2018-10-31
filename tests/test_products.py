import unittest

import os
import json
from smapi import create_app
from config import Config
from smapi.models.dbase import Databasehandler

db=Databasehandler()


class ProductTestCase(unittest.TestCase):
    def setUp(self):
        app=create_app(mode='testing')
        self.client= app.test_client()
        self.db=db
        self.samplepdt={
            "product_id":1,
            "product_name":"crocs",
            "unit_price": "3000"
        }
        

    def test_add_product(self):
        # db.add_pdt("cupps",30000)
        res=self.client.post('/api/v2/products', data=json.dumps(self.samplepdt),
        content_type='application/json')
        
        self.assertEqual(res.status_code,401)
        
    def test_fetch_all_products(self):
        res=self.client.post('/api/v2/products', data=json.dumps(self.samplepdt),
        content_type='application/json')
        self.assertEqual(res.status_code,401)
        res= self.client.get('/api/v2/products')
        self.assertEqual(res.status_code,404)
        
    def test_fetch_product_by_id(self):
        
        result = self.client.get(
            '/api/v2/products/1')
        self.assertEqual(result.status_code, 404)
        
    def test_product_can_be_edited(self):

        rv = self.client.post(
            '/api/v2/products/',
            data={
                "product_id":1,
                "product_name":"crocs",
                "unit_price": "3000"})
        self.assertEqual(rv.status_code, 401)
        rv = self.client.put(
            '/api/v2/products/1',
            data={
                "unit_price":"5000"
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client.get('/api/v2/products/1')
        self.assertIn("5000", str(results.data))
        

    def test_product_deletion(self):
        rv = self.client.post(
            '/api/v2/products/',
            data={
                "product_id":1,
                "product_name":"crocs",
                "unit_price": "3000"})
        self.assertEqual(rv.status_code, 401)
        res = self.client.delete('/api/v2/products/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client.get('/api/v2/products/1')
        self.assertEqual(result.status_code, 404)
        

if __name__ == "__main__":
    unittest.main()