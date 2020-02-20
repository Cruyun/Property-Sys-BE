'''
  /profile/:id/  获取用户个人信息
'''
from flask import jsonify, request, g
from . import api
from ..models import User
from ..decorators import login_required

@api.route('')

