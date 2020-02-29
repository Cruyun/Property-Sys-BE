from functools import wraps
from flask import g, jsonify, request
from .models import User

def login_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    token = request.headers.get('token')
    if token is not None:
      g.current_user = User.verify_auth_token(token)
      if g.current_user is not None:
        return f(*args, **kwargs)
      return jsonify({"message": "not such user!"}), 401
    return jsonify({"message": "no token!"}), 401
  return  decorated
