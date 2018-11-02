from flask import Flask, Request, json, jsonify, request,Blueprint,current_app as app
from flask_jwt_extended import get_jwt_identity, jwt_required

from smapi.models.dbase import Databasehandler
from smapi.views.vatlidators import Validation

sale = Blueprint("sale",__name__)

validator=Validation()

@sale.route('/api/v2/sales',methods=['POST'])
@jwt_required
def add_sale_order():
    db = Databasehandler()
    current_user = get_jwt_identity()
    sale_data = request.get_json()
    product_id= sale_data['product_id']
    entered_by = sale_data['entered_by']
    cost = sale_data['cost']
    quantity = sale_data['quantity']
    total = sale_data['total']
    
    invalid_sale=validator.sale_validate(product_id,entered_by,quantity)
    if current_user == 'false':
        if invalid_sale:
            return jsonify({"message": invalid_sale}), 400
        db.get_a_pdt(product_id) 
        db.create_saleorder(product_id,entered_by,cost,quantity,total)
        return jsonify({'You have sold':f'{quantity} of {product_id}'})
    return jsonify({"message":"Access denied, Log in as attendant to add sale orders."}), 401


@sale.route('/api/v2/sales', methods=['GET'])
def fetch_sales():
    db = Databasehandler()
    sales= db.get_sales()   
    if len(sales)<1:
        return jsonify({
            "status":'Fail',
            "message":'There are no sale orders'
        }),404

    if len(sales)>=1:
        return jsonify({
            "Sale_orders":sales
        }),200
 
@sale.route('/api/v2/sales/<int:sale_id>',methods=['GET'])
def fetch_a_single_sale(sale_id):
    db = Databasehandler()
    sale=db.get_a_sale(sale_id)
    return jsonify({'Sale order':sale}),200