from flask import request
from uuid import uuid4
from flask.views import MethodView

from schemas import PostSchema
from db import posts, users
from . import bp
# post routes

@bp.route('/<post_id>')
class Post(MethodView):

  @bp.response(200, PostSchema)
  def get(self, post_id):
    try:
      return posts[post_id]
    except KeyError:
      return {'message': "Invalid Post"}, 400

  @bp.arguments(PostSchema)
  def put(self, post_data ,post_id):
    try:
      post = posts[post_id]
      if post_data['user_id'] == post['user_id']:
        post['body'] = post_data['body']
        return { 'message': 'Post Updated' }, 202
      return {'message': "Unauthorized"}, 401
    except:
      return {'message': "Invalid Post Id"}, 400

  def delete(self, post_id):
    try:
      del posts[post_id]
      return {"message": "Post Deleted"}, 202
    except:
      return {'message':"Invalid Post"}, 400

@bp.route('/')
class PostList(MethodView):

  @bp.response(200, PostSchema(many = True))
  def get(self):
    return  list(posts.values())
  
  @bp.arguments(PostSchema)
  def post(self, post_data):
    user_id = post_data['user_id']
    if user_id in users:
      posts[uuid4()] = post_data
      return { 'message': "Post Created" }, 201
    return { 'message': "Invalid User"}, 401
