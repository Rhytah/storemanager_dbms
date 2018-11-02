from flask import Flask, Request, json, jsonify, request,Blueprint, current_app as app
from flask_jwt_extended import JWTManager
from smapi.models.dbase import Databasehandler
from flask_jwt_extended import get_jwt_identity, jwt_required

from smapi.models.product_model import Product
from smapi.models.user_model import User

import re
from smapi.views.vatlidators import Validation

product = Blueprint("product",__name__)

validator=Validation()



@product.route("/api/v2/products", methods =["POST"])
@jwt_required
def add_products():
    db = Databasehandler()
    current_user = get_jwt_identity()
    if current_user == 'admin':
        request_data=request.get_json()
        product_name= request_data.get('product_name')
        unit_price = request_data.get('unit_price')
        category = request_data.get('category')
        stock = request_data.get('stock')
        invalid=validator.product_validate(product_name,unit_price,category,stock)
        if invalid:
            return jsonify({"message": invalid}), 400 
            
        db.add_pdt(product_name,unit_price,category,stock)
        return jsonify({"message":"Product successfully added"})
    return jsonify({"message":"Access denied, Log in as admin to add Products"}), 401

@product.route('/api/v2/products', methods=['GET'])
def fetch_products():
    db = Databasehandler()
    products= db.get_pdts()   
    if len(products)<1:
        return jsonify({
            "status":'Fail',
            "message":'There are no products'
        }),404

    if len(products)>=1:
        return jsonify({
            "message":'Available products',
            "product":products
        }),200

@product.route('/api/v2/products/<int:product_id>',methods=['GET'])
def fetch_a_specific_product(product_id):
    db = Databasehandler()
    product=db.get_a_pdt(product_id)
    return jsonify({'Product':product})

@product.route('/api/v2/products/<int:product_id>', methods=['DELETE'])
def remove_product(product_id):
    db = Databasehandler()
    db.delete_product(product_id)
    return jsonify({
        "message":"You have deleted product",
    })

@product.route('/api/v2/products/<int:product_id>', methods=['PUT'])
def modify_product(product_id):
    db = Databasehandler()
    request_data=request.get_json()
    product_name = request_data['product_name']
    unit_price=request_data['unit_price']
    stock = request_data['stock']
    invalid=validator.product_mod(product_name,unit_price,stock)
    if invalid:
        return jsonify({"message": invalid}), 400 
    db.update_product(product_id,product_name, unit_price, stock)
    return jsonify({"message":"Successfully updated product"})