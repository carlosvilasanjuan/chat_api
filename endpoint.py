from flask import Flask, request, render_template
from app import app
from pymongo import MongoClient
from helpers.mongo import insert_data, get_id
from bson.objectid import ObjectId
from bson.json_util import dumps

client = MongoClient()
db = client.get_database("chat")

app = Flask(__name__)

@app.route('/')
def welcome():
    return "WELCOME TO THE SENTIMENT INTENSITY ANALYSIS PLATFORM"


# Create Username
@app.route('/create/user/')
def create_user():    
    username = request.args.get('username')
    user_json = {'username':username}
    user = db.users.insert_one(user_json)
    user_id = db.users.find({'username':username})
    return dumps(user_id)

# Create chat
@app.route('/create/chat/')
def create_chat():    
    subject = request.args.get('subject')
    voices = request.args.getlist('voices')  
    chat_json = {"subject":subject,"voices":voices}
    chat = db.chats.insert_one(chat_json)
    chat_id = db.chats.find({"subject":subject})
    return dumps(chat_id)


# Create Message
@app.route('/chat/<chat_id>/addmessage')
def create_message(chat_id):
    chat_id = ObjectId(chat_id)
    user_id = ObjectId(request.args.get("user_id"))
    text = request.args.get("text")
    message_json = {"chat_id":chat_id, "user_id":user_id, "text":text}
    message = db.messages.insert_one(message_json)
    message_id = db.messages.find({"text":text})
    return dumps(message_id)

#
@app.route('/chat/<chat_id>/list')
def get_list(chat_id):
    chat_id = ObjectId(chat_id)
    chat_list =  db.messages.find({"chat_id":chat_id}, {"_id":0,"user_id":1, "text":1})
    return dumps(chat_list)

app.run(debug=True)


