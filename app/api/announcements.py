'''
  /announces/:id/ 查看某小区的公告
  /announce/:id/ 查看一条公告
  /announce/ 发布公告
  /announce/  编辑公告
  /announce/ 删除公告
'''

from flask import jsonify, request, g
from . import api
from ..models import User, Announcement
from ..decorators import login_required
from .. import db

@api.route('/announces/', methods=['GET'])
def announces():
  eid = request.args.get('id')
  announcement_list = Announcement.query.filter_by(estate_id=eid).order_by(Announcement.time.desc()).all()

  return jsonify({
      "message": "success",
      "announces": [announce.to_json() for announce in announcement_list]
    }), 200

@api.route('/announce/', methods=['GET'])
def announce():
  aid = request.args.get('id')
  announcement = Announcement.query.filter_by(id=aid).first()
  t = announcement.time
  time = "%s-%s %s:%s:%s" % (t.year, t.month, t.hour, t.minute, t.second)

  if announcement is None:
    return jsonify({
        "message": "announcement is not exist"
      }), 404
  return jsonify({
    "message": "success",
    "content": announcement.content,
    "title": announcement.title,
    "time": announcement.time
    })

@api.route('/announce/', methods=['POST'])
@login_required
def post_announce():
  user = User.query.filter_by(id=g.current_user.id).first()

  is_admin = user.is_admin
  if is_admin is False:
    return jsonify({
        "message": "no permission to post"
      }), 403

  content = request.get_json().get('content')
  title = request.get_json().get("title")
  # 待处理时间？
  time = request.get_json().get("time")
  estate_id = user.estate_id

  annouce = Announcement(
        content = content,
        title = title,
        time = time,
        estate_id = estate_id
      )
  db.session.add(annouce)
  db.session.commit()
  return jsonify({
      "message": "success"
    }), 200


@api.route('/announce/', methods=['PUT'])
@login_required
def edit_annouce():
  aid = request.args.get('id')
  announce = Annoucement.query.filter_by(id=aid).first()

  if announce is None:
    return jsonify({
        "message": "announce does not exist"
      }), 404
  content = request.get_json().get('content')
  title =  request.get_json().get("title")
  announce.content = content
  announce.title = title
  db.session.add(announce)
  db.session.commit()
  return jsonify({
      "message": "success"
    }), 200

@api.route('/announce/', methods=['DELETE'])
@login_required
def delete_announce():
  aid = request.get_json().get("id")
  announce = Announcement.query.filter_by(id=aid).first()
  user = User.query.filter_by(id=g.current_user.id).first()
  is_admin = user.is_admin

  if announce is None:
    return jsonify({
      "message": "announce does not exist"
      }), 404
  if is_admin is False:
    return jsonify({
      "message": "no permission"
      }), 403
  db.session.delete(announce)
  db.session.commit()
  return jsonify({
    "message": "success",
    }), 200

