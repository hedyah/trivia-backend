
from flask import jsonify,request
from helper.dbhelpers import run_query
from app import app

#to create a quiz
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

    return jsonify ("Created Quiz sucessfully!"),200

# to activiate the quiz if there are a minimum of 5 questions
@app.patch('/api/quizzes')
def quiz_patch():
    data = request.json
    quiz_id = data.get('quiz_id')
    
    if not quiz_id:
        return jsonify("Missing requires arguments: quiz_id"),422
    #db write
    
    run_query("UPDATE quizzes SET active=1 WHERE id=?", [quiz_id])
    
    return jsonify("Updated the quiz sucessfully! THe quiz is now active"),200

#to create questions and answers
@app.post('/api/questions')
def questions_post():
    data = request.json
    trivia_question = data.get('trivia_question')
    image_url = data.get('image_url')
    answer_content= data.get('answer_content').get('answer')
    answer_wrong= data.get('answer_wrong')
    image_answer_url = data.get('answer_content').get('img')
    quiz_id = data.get('quiz_id')
    
    if not answer_content:
        return jsonify("Missing requires arguments: answer_content"),422
    if not trivia_question:
        return jsonify("Missing required argument: trivia_question"),422
    if not image_url:
        return jsonify("Missing required argument : image_url"),422
    #db write
    
    question = run_query("INSERT INTO questions (trivia_question,image_url, quiz_id) VALUES (?,?,?)", 
                [trivia_question,image_url, quiz_id])
    #db write
    
    run_query("INSERT INTO answers (content,image_answer_url, question_id, correct) VALUES(?,?,?,?)",
                [answer_content,image_answer_url,question,1])
    
    for answer in answer_wrong:
        ans_wrong= answer.get('answer')
        img = answer.get('img')
        run_query("INSERT INTO answers (content,image_answer_url, question_id, correct) VALUES(?,?,?,?)",[ans_wrong,img,question,0])
    

    return jsonify ('Created quiz questions sucessfully',200)
    



#to grab all the quizzes
@app.get('/api/quizzes')
def quiz_get():
    quizzes= run_query("SELECT * From quizzes Where active=?",[1])
    if quizzes == []:
        return jsonify('NO Quizzes Active!')
    get_content = run_query("SELECT * From quizzes")
    resp = []
    for content in quizzes:
        obj = {}
        obj['quiz_id']= content[0]
        obj['quiz_name'] = content[1]
        obj['points']= content[2]
        obj['genre_id']=content[3]
        obj['active']=content[4]
        
        resp.append(obj)
    if not quizzes:
        return jsonify("Error, couldn't reach your request!"),422
    return jsonify(resp),200

#to grab all the questions and answers
@app.get('/api/questions')
def questions_get():

    
    get_content = run_query("SELECT id, trivia_question, image_url, quiz_id FROM questions")
    resp = []
    for content in get_content:
        obj = {}
        obj['question_id']= content[0]
        obj['question'] = content[1]
        obj['image_url']= content[2]
        obj['quiz_id']=content[3]

        
        obj['answers']=[]
        answers = run_query("SELECT id, content, correct, image_answer_url FROM answers WHERE question_id=?",[content[0]])
        for answer in answers:
            answer_obj= {}
            answer_obj['answer_id']=answer[0]
            answer_obj['answer']=answer[1]
            answer_obj['correct']=answer[2]
            answer_obj['image_answer_url']=answer[3]
            obj['answers'].append(answer_obj)
        resp.append(obj)
    
    if not get_content:
        return jsonify("Error, couldn't reach your request!"),422
    return jsonify(resp),200