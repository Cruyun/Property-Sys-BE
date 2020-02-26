'''
  /profile/:id/  查看用户个人信息
  /profile/edit/:id/ 编辑用户个人信息
'''
from flask import jsonify, request, g
from . import api
from ..models import User, Estate, Room
from ..decorators import login_required
from .. import db, app

@api.route('/profile/', methods=["GET"])
@login_required
def profile():
  user = User.query.filter_by(id=g.current_user.id).first()
  eid = user.estate_id
  estate = Estate.query.filter_by(id=eid).first().name
  room = Room.query.filter_by(id=user.room_id).first().name
  parking = Parking.query.filter(id=user.parking_id).first().address

  if user is None:
    return jsonify({
       "message": "user does not exist!"
      }), 404
  return jsonify({
      "message": "success",
      "username": user.username,
      "is_admin": user.is_admin,
      "telephone" user.telephone,
      "car_no": user.car_no,
      "estate": estate,
      "room": room,
      "parking": parking
    }), 200

@api.route('/profile/edit/', methods=['PUT'])
@login_required
def editprofile():
  user_id = request.args.get("id")
  user = User.query.filter_by(id=user_id).first()

  if user is None:
    return jsonify({
        "message" : "user doest not exist!"
      }), 404
  if user_id is not g.current_user.id:
    return jsonify({
      "message": "no permission to edit"
      }), 403
  username = request.get_json().get("username")
  telephone = request.get_json().get("telephone")
  car_no = request.get_json().get("car_no")
  room_id = request.get_json().get("room_id")
  parking_id = request.get_json().get("parking_id")

  if username is not None:
    user.username = username
  if telephone is not None:
    user.telephone = telephone
  if car_no is not None:
    user.car_no = car_no
  if room_id is not None:
    user.room_id = room_id
  if parking is not None:
    user.parking_id = parking_id

  db.session.add(user)
  db.session.commit()
  return jsonify(
      "message" : "edit successfully!",
      {}), 200
  

