from flask import Flask, request
from uuid import uuid4

app = Flask(__name__)

users = {
  '1': {
    'username': 'dsmith',
    'email' : 'dsmith@ct.com'
  },
  '2' : {
    'username': "brandtc",
    'email': 'brandtc@ct.com'
  }
}

posts = {
  '1' : {
    'body' : 'FLASK WEEK LETS GO!!!',
    'user_id': '1'
  },
  '2': {
    'body': "Whiteboard was killer",
    'user_id': '2'
  },
  '3':{
    'body': 'SERVERS!!!!',
    'user_id' : '2'
  }
}

""" 
Create - Post
Retrieve - Get
Update 
Delete
 """


# user routes

@app.get('/user')
def user():
  return { 'users': list(users.values()) }, 200

@app.route('/user', methods=["POST"])
def create_user():
  json_body = request.get_json()
  users[uuid4()] = json_body
  return { 'message' : f'{json_body["username"]} created' }, 201

@app.put('/user/<user_id>')
def update_user(user_id):
  try:
    user = users[user_id]
    user_data = request.get_json()
    user |= user_data
    return { 'message': f'{user["username"]} updated'}, 202
  except KeyError:
    return {'message': "Invalid User"}, 400
      
@app.delete('/user/<user_id>')
def delete_user(user_id):
  # user_data = request.get_json()
  # username = user_data['username']
  try:
    del users[user_id]
    return { 'message': f'User Deleted' }, 202
  except:
    return {'message': "Invalid username"}, 400

# post routes

@app.get('/post')
def get_posts():
  return { 'posts': list(posts.values()) }

@app.post('/post')
def create_post():
  post_data = request.get_json()
  user_id = post_data['user_id']
  if user_id in users:
    posts[uuid4()] = post_data
    return { 'message': "Post Created" }, 201
  return { 'message': "Invalid User"}, 401

@app.put('/post')
def update_post():
  return

@app.delete('/post')
def delete_post():
  return