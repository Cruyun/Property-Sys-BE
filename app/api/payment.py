'''
 /pay/ 缴费
 /fee/  查看余额
 /payment/ 查看缴费记录
'''

from flask import jsonify, request, g
from . import api
from ..models import User, Estate, Room, Payment
from ..decorators import login_required
from .. import db

@api.route('/pay/', Methods=['POST'])
@login_required
def pay():
  fee_type = request.get_json().get("fee_type")
  user_id = request.get_json().get("user_id")

  if g.current_user.id != user_id:
    return jsonify({
        "message": "no permission"
      }), 403

  user = User.query.filter_by(id=user_id).first()
  if user.room_id is None:
    return jsonify({
        "message": "user does not submit room"
      }), 404
  room = Room.query.filter_by(id=user.room_id).first()
  fee = request.get_json().get("fee")
  amount = request.get_json().get("amount")

  if fee_type == 0:
    room.water_uesd = 0
    room.water_fee = 0
  elif fee_type == 1:
    room.gas_fee = 0
    room.gas_amount = 0
  else:
    room.ele_fee = 0
    room.ele_amount = 0

  payment = Payment(
        state = 0,
        type = request.get_json().get("fee_type"),
        amount = amount,
        fee = fee,
        room_id = user.room_id,
        estate_id = user.estate_id
      )
  db.session.add(payment)
  db.session.add(room)
  db.session.commit()
  return jsonify({
      "message": "success"
    }), 200

@api.route('/fee/', Methods=['GET'])
@login_required
def fee():
  user_id = g.current_user.id
  user = User.query.filter_by(id=user_id).first()

  if user.room_id is None:
    return jsonify({
        "message": "user does not submit room"
      }), 404

  room = Room.query.filter_by(id=user.room_id).first()
  if room is None:
    return jsonify({
      "message": "room does not exist"
      }), 404
  return jsonify({
      "message": "success",
      "room": room.name,
      "room_id": room.id,
      "water_used": room.water_used,
      "water_fee": room.water_fee,
      "gas_used": room.gas_used,
      "gas_fee": room.gas_fee,
      "ele_used": room.ele_used
    }), 200

@api.route("/payment/", Methods=["GET"])
@login_required
def payment():
  page = request.args.get('page', 1, type=int)
  user = User.query.filter_by(id=g.current_user.id).first()
  
  payment_list = list(user.payment_record)

  per_page = 10
  start = (page-1)* per_page
  end = min(page*per_page, len(payment_list))
  payment_list = payment_list[start:end]
  return jsonify({
    "message": "success",
    "payment": [payment.to_json() for payment in payment_list]
    "count": len(payment_list)
    }), 200

