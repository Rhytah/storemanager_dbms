from flask import Flask, Request, json, jsonify, request
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)

from app import app
from smapi.models.sales_model import Sale
from smapi.models.user_model import User
from smapi.models.dbase import Databasehandler

app.config['JWT_SECRET_KEY'] = 'andela13' 

jwt = JWTManager(app)
db = Databasehandler()


@app.route('/api/v2/sales',methods=['POST'])
@jwt_required
def add_sale_order():
    current_user = get_jwt_identity()
    entered_by = current_user
    sale_data= request.get_json()
    if current_user == 'attendant':
        product_name=sale_data['product_name']
        unit_price = sale_data['unit_price']
        quantity = sale_data['quantity']

        db.add_sale(entered_by,product_name,unit_price,quantity) 
        
        return jsonify({'message':'sale_order has been posted'})
    return jsonify({"message":"Access denied, Log in as attendant to add sale orders."}), 401


@app.route('/api/v2/sales', methods=['GET'])
def fetch_sales():
    sales= db.get_sales()   
    if len(sales)<1:
        return jsonify({
            "status":'Fail',
            "message":'There are no products'
        }),404

    if len(sales)>=1:
        return jsonify({
            "message":'Available products',
            "Sale_orders":sales
        }),200
 


@app.route('/api/v2/sales/<int:sale_id>',methods=['GET'])
def fetch_a_single_sale(sale_id):
    sale=db.get_a_sale(sale_id)
    return jsonify({'Sale order':sale})
