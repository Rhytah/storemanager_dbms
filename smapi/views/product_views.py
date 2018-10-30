from flask import Flask, Request, json, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)

from app import app
from smapi.models.product_model import Product
from smapi.models.user_model import User
from smapi.models.dbase import Databasehandler
import re

app.config['JWT_SECRET_KEY'] = 'andela13' 
jwt = JWTManager(app)

db = Databasehandler()


@app.route("/api/v2/products", methods =["POST"])
@jwt_required
def add_products():
    current_user = get_jwt_identity()
    if current_user == 'admin':
        request_data=request.get_json()
        product_name= request_data.get('productName')
        unit_price = request_data.get('productPrice')

        if not product_name:
            return "Product Name is missing"
        if product_name == " ":
            return "Product Name is missing"
        if not re.match(r"^([a-zA-Z]+[-_\s])*[a-zA-Z]+$", product_name):
            return "product name must have no white spaces"
        if not re.match(r"^[0-9]*$", unit_price):
            return "Product price must be only digits and must have no white spaces"    
        if len(product_name) < 3:
            return "product name should be more than 4 characters long"
        if not unit_price:
            return "Product price is missing"
        if int(unit_price) < 1:
            return "Product price should be greater than zero"    
        if unit_price == " ":
            return "Product price is missing"    
        db.add_pdt(product_name,unit_price)
        return jsonify({"message":"Product successfully added"})
    return jsonify({"message":"Access denied, Log in as admin to add Products"}), 401

@app.route('/api/v2/products', methods=['GET'])
def fetch_products():
    products= db.get_pdts()   
    if len(products)<1:
        return jsonify({
            "status":'Fail',
            "message":'There are no products'
        }),404

    if len(products)>=1:
        return jsonify({
            "message":'Available products',
            "products":products
        }),200
 


@app.route('/api/v2/products/<int:product_id>',methods=['GET'])
def fetch_a_specific_product(product_id):
    product=db.get_a_pdt(product_id)
    return jsonify({'Product':product})
