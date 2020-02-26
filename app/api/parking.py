'''
/carno/:id/ 通过小区id 获取车位 id 列表
'''

from flask import jsonify, request, g
from . import api
from ..models import User
from ..decorators import login_required
from .. import db, app

