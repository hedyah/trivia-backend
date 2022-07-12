from flask import Flask

app = Flask(__name__)

from endpoints import client
from endpoints import client_session
from endpoints import quizzes
from endpoints import game