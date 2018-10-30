from flask import Flask, json, jsonify, request
from app import app
from smapi.models.user_model import User
from smapi.models.dbase import Databasehandler
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)

app.config['JWT_ACCESS_TOKEN_EXPIRES'] =False
app.config['JWT_SECRET_KEY'] = 'andela13' 
jwt = JWTManager(app)
db=Databasehandler()



@app.route('/api/v2/auth/login', methods =['POST'])
def login_user():
    user_data=request.get_json()
    username=user_data['username']
    password=user_data['password']
    
    if not username:
        return jsonify({"msg" : "Provide Valid Username"}),400

    if not password:
        return jsonify({"msg" : "Incorrect password"}),400
    # if role != "Owner" or "Attendant":
    #     return jsonify({"msg":"Role can only be either Owner or Attendant. Input valid role"})

    access_token= create_access_token(identity=username)
 
    return jsonify({
        "message":f"{username}, successfully logged in ",
        "access_token":access_token}),200

@app.route('/api/v2/auth/signup',methods=['POST'])
@jwt_required
def signup():
    current_user=get_jwt_identity()
    if current_user == 'admin':
        user_data=request.get_json()
        username=user_data['username']
        password=user_data['password']
    
        db.add_user(username,password)
        return jsonify({"message":f"{username} successfully added"})
    return jsonify({"message":"Only Admin can add users. Contact Application administrator"})

@app.route('/api/v2/protected', methods =['GET'])
@jwt_required
def protected():
    #access the identity of current user
    current_user=get_jwt_identity()
    return jsonify(loggesd_in_as=current_user),200
