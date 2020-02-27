'''
  /rooms/:id/ 通过小区 id 获取房间 id 与房间名
  /room/:id/ 获取住房详细信息（缴费时查询用）
'''

from flask import jsonify, request, g
from . import api
from ..models import Room
from ..decorators import login_required
from .. import db

@api.route('/rooms/', methods=['GET'])
def rooms():
  eid = request.args.get('estate_id')
  rooms = Room.query.filter_by(estate_id=eid).all()
  
  return jsonify({
    "message": "success",
    "rooms": [room.to_simple_json() for room in rooms]
    }), 200

@api.route('/room/', methods=['GET'])
def room_detail():
  rid = request.args.get('room_id')
  room = Room.query.filter_by(id=rid).first()

  if room is None:
    return jsonify({
      "message": " room does not exist"
      )}, 404
  return jsonify({
      "message": "success",
      "name": room.name,
      "water_fee": self.water_fee,
      "water_used": self.water_used,
      "gas_fee": self.gas_fee,
      "gas_used": self.gas_used,
      "ele_fee": self.ele_fee,
      "ele_used": self.ele_used,
    }), 200
