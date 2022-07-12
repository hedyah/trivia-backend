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

    checkuser = run_query("SELECT * FROM trivia_users WHERE email=? and password=?",[email,password])
    if checkuser == []:
        return jsonify("user not found!"),401
    user_id = checkuser[0][0]
    #db write select quiery that matches the email and password
    
    create_token = uuid.uuid4().hex
    print(create_token)
    run_query("INSERT INTO user_session (token,user_id) VALUES(?,?)",[create_token, user_id])
    #if it matches create a session token with uuid.uuid4
    
    return jsonify("User loggin in!"),200

@app.delete('/api/user-session')
def userSession_delete():
    data= request.json
    user_id = data.get('user_id')
    run_query("DELETE FROM user_session WHERE user_id=?",[user_id])