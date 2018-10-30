from flask import Flask, json, jsonify, request
from app import app
from smapi.models.user_model import User
from smapi.models.dbase import Databasehandler
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)


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

    access_token= create_access_token(identity=username)
 
    return jsonify({
        "message":f"{username}, successfully logged in",
        "access_token":access_token}),200

        

@app.route('/api/v2/protected', methods =['GET'])
@jwt_required
def protected():
    #access the identity of current user
    current_user=get_jwt_identity()
    return jsonify(loggesd_in_as=current_user),200
