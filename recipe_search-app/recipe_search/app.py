from flask import Flask, request
import awsgi
from recipe_search import recipe_search

app = Flask(__name__)
app.json.ensure_ascii = False

@app.route('/')
def get_request():
    request_ingredients = request.args.getlist('ingredients')
    return recipe_search(*request_ingredients)

def lambda_handler(event,context):
    return awsgi.response(app,event,context)