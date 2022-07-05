import uuid
from flask import jsonify, request
from helper.dbhelpers import run_query
import uuid
from app import app


#client_session API
@app.post('/api/user-session')
def userSession_post():
    
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email: 
        return jsonify("missing arguement requirement: email"),422
    if not password:
        return jsonify("missing argument requirement: password"),422

    checkuser = run_query("SELECT * FROM client WHERE email=? and password=?",[email,password])
    if checkuser == []:
        return jsonify("user not found!"),401
    user_id = checkuser[0][0]
    #db write select quiery that matches the email and password
    
    create_token = uuid.uuid4().hex
    print(create_token)
    run_query("INSERT INTO client_session (token,client_id) VALUES(?,?)",[create_token, user_id])
    #if it matches create a session token with uuid.uuid4
    
    # headers = request.headers
    # auth = headers.get("x-token")
    # if auth == create_token:
    #     return jsonify("user is authorized"),200
    # else:
    #     return jsonify("user is not authorized"),401
    
    #if it doesnt match say "404: Error the is no profile found"
    return jsonify("User loggin in!",[create_token]),200
    