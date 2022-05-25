# server wont start without flask
from flask import Flask 
app = Flask(__name__)

#secret key for cookie access, allows use of session
app.secret_key = "418171514"

# setting global variable for datatbase name
DATABASE = "prime_rhyme_time_schema"