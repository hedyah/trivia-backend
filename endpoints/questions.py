from flask import jsonify,request
from helper.dbhelpers import run_query
from app import app

@app.post('/api/questions')
def 