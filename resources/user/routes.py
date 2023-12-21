from flask import request
from uuid import uuid4

from . import bp
from db import users
# user routes

@bp.get('/user')
def user():
  return { 'users': list(users.values()) }, 200

@bp.get('/user/<user_id>')
def get_user(user_id):
  try:
    return { 'user': users[user_id] } 
  except:
    return {'message': 'invalid user'}, 400
    
@bp.route('/user', methods=["POST"])
def create_user():
  user_data = request.get_json()
  for k in ['username', 'email', 'password']:
    if k not in user_data:
      return {'message': "Please include username email and password"}, 400
  users[uuid4()] = user_data
  return { 'message' : f'{user_data["username"]} created' }, 201

@bp.put('/user/<user_id>')
def update_user(user_id):
  try:
    user = users[user_id]
    user_data = request.get_json()
    user |= user_data
    return { 'message': f'{user["username"]} updated'}, 202
  except KeyError:
    return {'message': "Invalid User"}, 400
      
@bp.delete('/user/<user_id>')
def delete_user(user_id):
  # user_data = request.get_json()
  # username = user_data['username']
  try:
    del users[user_id]
    return { 'message': f'User Deleted' }, 202
  except:
    return {'message': "Invalid username"}, 400