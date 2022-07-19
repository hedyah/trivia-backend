from flask import jsonify,request
from helper.dbhelpers import run_query
from app import app
import bcrypt

@app.post('/api/client')
def triviaUser_post():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    first_name = data.get('first_name')
    username = data.get('username')
    image_url = data.get('image_url')
    if not email:
        return jsonify("missing required arguement: email "),422
    if not password:
        return jsonify("missing required arguement: password "),422
    if not username:
        return jsonify("missing required arguement: username "),422
    if not first_name:
        return jsonify("missing required arguement: firstName"),422
    if not image_url:
        return jsonify("missing argument required: image_url"),422
    #hash password
    passwordinput = password
    salt =bcrypt.gensalt()
    hash_result = bcrypt.hashpw(passwordinput.encode(), salt)
    
    #DB write
    run_query("INSERT INTO trivia_users (email, password, username, first_name, image_url) VALUE(?,?,?,?,?)", 
                [email,password,username,first_name,image_url] )
    return jsonify("Post created sucessfully!"),200

@app.get('/api/client')
def triviaUser_get():
    headers = request.headers
    tokens = headers.get("token")
    if not tokens :
        
        return jsonify("user is not authorized"),401
    
    checkuser = run_query("SELECT user_id FROM user_session WHERE token=?", [tokens])
    if checkuser == []:
        return jsonify("user does not have access!"),401
    client_id = checkuser[0][0]
    get_content = run_query("SELECT id,email,username,first_Name,image_url from trivia_users WHERE id=?",[client_id])
    resp = []
    for content in get_content:
        obj = {}
        obj['id']= content[0]
        obj['email']= content[1]
        obj['username']= content[2]
        obj['firstName']= content[3]
        obj['image_url']= content[4]
        resp.append(obj)
    if not get_content:
        return jsonify("Error ,couldn't process get request!"),422
    return jsonify(resp),200

