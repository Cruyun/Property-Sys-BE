'''
  /estates/ 获取所有小区
'''
from flask import jsonify, request, g
from . import api
from ..models import Estate
from .. import db

@api.route("/estates/", methods=["GET"])
def all_estates():
  estates = Estate.query.all()
  estates = list(estates)

  return jsonify({
      "message": "success",
      "estates": estates
    }), 200

