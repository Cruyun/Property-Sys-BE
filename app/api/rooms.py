'''
  /rooms/:id/ 通过小区 id 获取房间 id 与房间名
  /room/:id/ 获取住房详细信息（缴费时查询用）
'''

from flask import jsonify, request, g
from . import api
from ..models import Room
from ..decorators import login_required
from .. import db, app

@api.route('/rooms/', methods=['GET'])
def rooms():
  eid = request.args.get('id')
  rooms = Room.query.filter_by(estate_id=eid).all()
  
  return jsonify({
    "message": "success",
    "rooms": [room.to_simple_json() for room in rooms]
    }), 200

@api.route('/room/<rid>/', methods=['GET'])
def room_detail():
  rid = request.args.get('rid')
  room = Room.query.filter_by(estate_id=rid).first()
