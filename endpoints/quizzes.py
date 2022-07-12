from flask import jsonify,request
from helper.dbhelpers import run_query
from app import app

@app.post('/api/quizzes')
def quiz_post():
    # headers = request.headers
    # tokens = headers.get("token")
    # if not tokens :
        
    #     return jsonify("user is not authorized"),401
    
    # checkuser = run_query("SELECT user_id FROM user_session WHERE token=?", [tokens])
    # if checkuser == []:
    #     return jsonify("user does not have access!"),401
    # client_id = checkuser[0][0]
    
    data = request.json
    quiz_name = data.get('quiz_name')
    quiz_genre = data.get('quiz_genre')
    quiz_points = data.get('quiz_points')
    
    if not quiz_name:
        return jsonify("Missing requires arguments: quiz_name"),422
    if not quiz_genre:
        return jsonify("Missing requires arguments: quiz_genre"),422
    if not quiz_points:
        return jsonify("Missing requires arguments: quiz_points"),422
    
    #DB write
    run_query("INSERT INTO quizzes (name, genre_id, points) VALUE(?,?,?)",
                [quiz_name,quiz_genre,quiz_points])
    
    # quiz_id=quiz [0][0]
    
    # quizz_id= run_query("SELECT quiz_id FROM quizzes WHERE quiz_name=?", [quiz_name])

    return jsonify ("Post created sucessfully!"),200

@app.post('/api/questions')
def questions_post():
    data = request.json
    trivia_question = data.get('trivia_question')
    image_url = data.get('image_url')
    answer_content= data.get('answer_content')
    image_answer_url = data.get('image_answer_url')
    quiz_name = data.get('quiz_name')
    
    if not answer_content:
        return jsonify("Missing requires arguments: answer_content"),422
    if not trivia_question:
        return jsonify("Missing required argument: trivia_question"),422
    if not image_url:
        return jsonify("Missing required argument : image_url"),422
    #db write
    quiz_id= run_query("SELECT quiz_id FROM quizzes WHERE quiz_name=?", [quiz_name])
    run_query("INSERT INTO questions (trivia_question,image_url, quiz_id) VALUE (?,?,?)", 
                [trivia_question,image_url, quiz_id])
    #db write
    question_id = run_query("SELECT question_id FROM questions WHERE quiz_id=? ",[quiz_id])
    run_query("INSERT INTO answers ( content,image_answer_url) VALUE(?,?)",
                [answer_content,image_answer_url])
    

    return jsonify ('Posted sucessfully',200)
    




@app.get('/api/trivia-quizzes')
def quiz_get():
    get_content = run_query("SELECT * from questions")
    resp = []
    for content in get_content:
        obj = {}
        obj['id']= content[0]
        obj['triviaQuestion'] = content[1]
        obj['image_url']= content[2]
        resp.append(obj)
    if not get_content:
        return jsonify("Error, couldn't reach your request!"),422
    return jsonify(resp),200