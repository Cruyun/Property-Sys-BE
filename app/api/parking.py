'''
  /free/:id/ 通过小区id 获取 空闲车位 id 列表
  /park/:id/ 占车位
  /park
'''

from flask import jsonify, request, g
from . import api
from ..models import User
from ..decorators import login_required
from .. import db, app

