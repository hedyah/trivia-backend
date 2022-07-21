import uuid
from flask import jsonify, request
from helper.dbhelpers import run_query
import uuid
from app import app


#client_session API login
@app.post('/api/client-session')
def userSession_post():
    
    data = request.json
    email = data.get('email')
    password = data.get('password')
    if not email: 
        return jsonify("missing arguement requirement: email"),422
    if not password:
        return jsonify("missing argument requirement: password"),422

    checkuser = run_query("SELECT * FROM trivia_users WHERE email=? and password=?",[email,password])
    if checkuser == []:
        return jsonify("user not found!"),401
    user_id = checkuser[0][0]
    #db write select quiery that matches the email and password
    
    create_token = uuid.uuid4().hex
    print(create_token)
    run_query("INSERT INTO user_session (token,user_id) VALUES(?,?)",[create_token, user_id])
    #if it matches create a session token with uuid.uuid4
    
    return jsonify([create_token]),200

#for the client to log out
@app.delete('/api/client-session')
def userSession_delete():
    
    headers = request.headers
    tokens = headers.get("token")
    if not tokens :
        
         return jsonify("Token is missing"),401
    
    checkuser = run_query("DELETE FROM user_session WHERE token=?", [tokens])
    if checkuser == []:
          return jsonify("user not found!"),401
    # client_id = checkuser[0][0]
    
    return jsonify("User logged out!"),200