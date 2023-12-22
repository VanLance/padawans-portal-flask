from flask import request
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from models.PostModel import PostModel
from schemas import PostSchema
from db import posts, users
from . import bp
# post routes

@bp.route('/<post_id>')
class Post(MethodView):

  @bp.response(200, PostSchema)
  def get(self, post_id):
    post = PostModel.query.get(post_id)
    if post:
      return post 
    abort(400, message='Invalid POst')

  @bp.arguments(PostSchema)
  def put(self, post_data ,post_id):
    post = PostModel.query.get(post_id)
    if post:
      post.body = post_data['body']
      post.commit()
    return {'message': "Invalid Post Id"}, 400

  def delete(self, post_id):
    post = PostModel.query.get(post_id)
    if post:
      post.delete()
      return {"message": "Post Deleted"}, 202
    return {'message':"Invalid Post"}, 400

@bp.route('/')
class PostList(MethodView):

  @bp.response(200, PostSchema(many = True))
  def get(self):
    return PostModel.query.all()
  
  @bp.arguments(PostSchema)
  def post(self, post_data):
    try:
      post = PostModel()
      post.user_id = post_data['user_id']
      post.body = post_data['body']
      post.commit()
      return { 'message': "Post Created" }, 201
    except:
      return { 'message': "Invalid User"}, 401
