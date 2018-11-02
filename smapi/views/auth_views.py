from flask import Flask, json, jsonify, request,Blueprint, current_app as app
from smapi.models.user_model import User

from flask_jwt_extended import (JWTManager,create_access_token,
                                get_jwt_identity, jwt_required)

from smapi.models.dbase import Databasehandler
import re
from smapi.views.vatlidators import Validation


auth = Blueprint("auth",__name__)

validate=Validation()

# db=Databasehandler()
@auth.route('/')
@auth.route('/index')
def index():
    return "StoreManager auth. Manage your Products and Sales efficiently using DBMS"


@auth.route('/api/v2/auth/login', methods =['POST'])
def login_user():
    db = Databasehandler()
    user_data=request.get_json()
    username=user_data['username']
    password=user_data['password']
    role = user_data['role']
    user=db.search_user(username)
    invali =validate.login_credits(username,password,role)
    if invali:
        return jsonify({"message": invali}), 400 

    if username==user.get('username') and password==user.get('password'):

        access_token= create_access_token(identity=role)
 
        return jsonify({
            "message":f"{username}, successfully logged in ",
            "access_token":access_token}),200
    return jsonify({"message":"Invalid credentials"})

@auth.route('/api/v2/auth/signup',methods=['POST'])
@jwt_required
def signup():
    db = Databasehandler()
    current_user=get_jwt_identity()
    if current_user == 'true':
        user_data=request.get_json()
        username=user_data['username']
        password=user_data['password']
        user=db.search_user(username)
        if username==user.get('username'):
            return jsonify({"message":"user already exists"})
        if not username:
            return "username is missing"
        if username == " ":
            return "username is missing"
        if not re.match(r"^([a-zA-Z]+[-_\s])*[a-zA-Z]+$", username):
            return "username must have no white spaces"
           
        if len(username) < 5:
            return "username should be more than 4 characters long"
    
        db.add_user(username,password)
        return jsonify({"message":f"-{username}- successfully added, to use password -{password}-"})
    return jsonify({"message":"Only Admin can add users. Contact application administrator"})

@auth.route('/api/v2/auth/users', methods=['GET'])
@jwt_required
def fetch_users():
    db = Databasehandler()
    current_user=get_jwt_identity()
    if current_user == 'true':
        users= db.get_users()   
        if len(users)<1:
            return jsonify({
                "status":'Fail',
                "message":'You have no staff'
            }),404

        if len(users)>=1:
            return jsonify({
                "message":'Store staff',
                "view":users
            }),200
    return jsonify({"message":"You are not the Admin"})

@auth.route('/api/v2/auth/users/<int:user_id>', methods=['PUT'])
@jwt_required
def assign_admin_rights(user_id):
    db = Databasehandler()
    current_user = get_jwt_identity()
    user_data=request.get_json()
    role = user_data['role']
    if current_user == 'true':
        
        db.promote_user(user_id,role)
        return jsonify({"message":f"You have promoted user to admin status"})
    return jsonify({"Auth Failure":"Log in as Admin to promote users"})

@auth.route('/api/v2/protected', methods =['GET'])
@jwt_required
def protected():
    #access the identity of current user
    current_user=get_jwt_identity()
    return jsonify(loggesd_in_as=current_user),200