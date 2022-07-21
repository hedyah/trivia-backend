from flask import jsonify,request
from helper.dbhelpers import run_query
from app import app

@app.post('/api/game')
def game_post():
    # headers = request.headers
    # tokens = headers.get("token")
    # if not tokens :
        
    #     return jsonify("user is not authorized"),401
    
    # checkuser = run_query("SELECT user_id FROM user_session WHERE token=?", [tokens])
    # if checkuser == []:
    #     return jsonify("user does not have access!"),401
    # client_id = checkuser[0][0]
    
    data= request.json
    user_id= data.get('user_id')
    quiz_id=data.get('quiz_id')
    points=data.get('points')
    question_id=data.get('question_id')
    answer_id= data.get('answer_id')
    
    
    
    # if not question_id:
    #     return jsonify("Missing requires arguments: question_id"),422
    if not answer_id:
        return jsonify("Missing requires arguments: answer_id"),422
    
    # When user answers a question, check the question and answer table to make sure its correct
    checkAnswer=run_query("SELECT id,correct FROM answers WHERE id=? and correct=?",[answer_id,1])
    if checkAnswer == []:
        return jsonify ({"correct":False}),200
    
    #when the user finishes the quiz then insert the score into the scoreboard
    #DB write
    else:
        run_query("INSERT INTO scoreboard (user_id, quiz_id, points) VALUES(?,?,?)",
                [user_id,quiz_id,points])
        return jsonify ({"correct":True}),200
    
#the scoreboard for the game 
@app.get('/api/game')
def get_score():
    get_content = run_query("SELECT scoreboard.id, points, user_id, quiz_id, trivia_users.id, username FROM scoreboard INNER JOIN trivia_users ON scoreboard.user_id=trivia_users.id")
    
    resp = []
    for content in get_content:
        obj = {}
        obj['id']= content[0]
        obj['points'] = content[1]
        obj['user_id']= content[2]
        obj['quiz_id']=content[3]
        obj['user_id']=content[4]
        obj['username']=content[5]
        
        
        # obj['answers']=[]
        # answers = run_query("SELECT id, content, correct, image_answer_url FROM answers WHERE question_id=?",[content[0]])
        # for answer in answers:
        #     answer_obj= {}
        #     answer_obj['answer_id']=answer[0]
        #     answer_obj['answer']=answer[1]
        #     answer_obj['correct']=answer[2]
        #     answer_obj['image_answer_url']=answer[3]
        #     obj['answers'].append(answer_obj)
        resp.append(obj)
    
    if not get_content:
        return jsonify("Error, couldn't reach your request!"),422
    return jsonify(resp),200