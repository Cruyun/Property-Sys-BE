'''
  /parkings/ 通过小区id 获取非私有车位列表
  /free/:id/ 通过小区id 获取 空闲车位列表
  /park/:id/ 占车位
  /leave/ 释放车位
  /tempfree/ 私有车位的业主开放/关闭临时可停车
  /check/ 查看私人车位是否开放
'''

from flask import jsonify, request, g
from . import api
from ..models import User, Parking, Estate
from ..decorators import login_required
from .. import db

@api.route("/parkings/", Methods=["GET"])
def public_parkings():
  estate_id = request.args.get("estate_id")
  parkings = Parking.query.filter_by(
        estate_id = estate_id,
        is_private = False
      )
  parkings = list(parkings)
  return jsonify({
      "message": "success",
      "public_parkings": parkings
    }), 200

@api.route("/free/", Methods=["GET"])
def free_parkings():
  estate_id = request.args.get("estate_id")
  parkings = Parking.query.filter_by(
      estate_id = estate_id,
      state = 0
      )
  parkings = list(parkings)
  return jsonify({
    "message": "success",
    "free_parkings": parkings
    }), 200

@api.route("/park/", Methods=["PUT"])
def park():
  user_id = g.current_user.id

  parking_id = request.get_json().get("parking_id")
  parking = Parking.query.filter_by(id=parking_id).first()

  if parking is None:
    return jsonify({
      "message": "parking does not exist"
      }), 404
  if parking.state == 1:
    return jsonify({
      "message": "parking is not free"
      }), 404
  car_no = request.get_json().get("car_no")

  already_park = Parking.query.filter_by(park_car_no=car_no).first()
  if already_park != None:
    return jsonify({
        "message": "car has already parked"
      }), 404

  parking.park_car_no = car_no
  parking.state = 1
  return jsonify({
    "message": "success"
    }), 200

@api.route("/leave/", Methods=["PUT"])
def leave():
  car_no = request.get_json().get("car_no")
  parking = Parking.query.filter_by(park_car_no=car_no).first()
  
  if parking is None:
    return jsonify({
        "message": "car has not yet parked"
      }), 404
  parking.state = 0
  parking.park_car_no = None
  db.session.add(parking)
  db.session.commit()
  return jsonify({
      "message": "success"
    }), 200

  
@api.route("/tempfree/", Methods=["PUT"])
@login_required
def tempfree():
  user_id = g.curren_user.id
  if user_id != request.get_json().get("user_id"):
    return jsonify({
        "message": "no permission"
      }), 403
  user = User.query.filter_by(id=user_id).first()
  parking_id = user.parking_id
  if parking_id is None:
    return jsonify({
        "message": "user has not yet submit parking"
      }), 404
  free = request.get_json().get("free")
  parking = Parking.query.filter_by(id=parking_id).first()
  
  if parking is None:
    return jsonify({
        "message": "parking does not exist"
      }), 200
  # 开放
  if parking.state == 1:
    parking.state = 0
    parking.park_car_no = None

  # 关闭
  if parking.state == 0:
    parking.state = 1
    if user.car_no != None:
      parking.park_car_no = user.car_no
  
  return jsonify({
      "message": "success"
    }), 200

@api.route("/check/", Methods=["GET"] )
@login_required
def checkfree():
  parking_id = request.get_json().get("parking_id")
  parking = Parking.query.filter_by(id=parking_id).first()

  if parking is None:
    return jsonify({
        "message": "parking does not exist"
      }), 200

  return jsonify({
      "message": "success",
      "state": parking.state
    }), 200


  
