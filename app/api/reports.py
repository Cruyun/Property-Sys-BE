'''
  /repo/ 查看 repo
  /repo/ 用户 编辑/ 管理员回复 repo
  /repo/ 提交 repo
  /repo/ 删除 repo
  /repos/ 用户查看自己的 repo 记录列表
  /repolist/ 管理员查看小区的 repo 记录列表
  /adminrepo/ 管理员重看自己正在处理的记录列表
'''
from flask import jsonify, request, g
from . import api
from ..models import User, Estate, Room, Report
from ..decorators import login_required
from .. import db, app

@api.route('/repo/', Methods=['GET'])
@login_required
def view_repo():
  repo_id = request.args.get("repo_id")
  repo = Report.query.filter_by(id=repo_id).first()

  user_id = repo.user_id
  username = User.query.filter_by(id=user_id).first().username or None

  admin_id = repo.admin_id
  admin = ''
  if admin_id != None:
    admin = User.query.filter_by(id=admin_id).first().username

  if repo is None:
    return jsonify({
        "message": "repo does not exist!"
      }), 404
  return jsonify({
      "message": "success",
      "content": repo.content,
      "state": repo.state,
      "repo_type": repo.repo_type,
      "admin_response": repo.admin_response,
      "submit_time": repo.submit_time,
      "solved_time": repo.solved_time,
      "username": username,
      "admin": admin
    }), 200

@api.route('/repo/', Methods=['PUT'])
@login_required
def edit_repo():
  repo_id = request.args.get("repo_id")
  repo = Report.query.filter_by(id=repo_id).first()

  if repo is None:
    return jsonify({
      "message": "repo does not exist!"
      }), 200

  content = request.get_json().get('content')
  state = request.get_json().get("state")
  repo_type = request.get_json().get("repo_type")
  admin_reponse = request.get_json().get("admin_response")
  solved_time = request.get_json().get("solved_time")
  admin_id = request.get_json().get("admin_id")

  if content != None:
    repo.content = content
  if state != None:
    repo.state = state
  if repo_type != None:
    repo.repo_type = repo_type
  if admin_response != None:
    repo.admin_response = admin_response
  if solved_time != None:
    repo.solved_time = solved_time
  if admin_id != None:
    repo.admin_id = admin_id

  db.session.add(repo)
  db.session.commit()
  return jsonify({
      "message": "success"
    }), 200

@api.route('/repo/', Methods=['POST'])
@login_required
def post_repo():
  content = request.get_json().get('content')
  repo_type = request.get_json().get("repo_type")
  user_id = request.get_json().get("user_id")
  estate_id = request.get_json().get("estate_id")

  repo = Report(
        content = content,
        repo_type = repo_type,
        user_id = user_id,
        estate_id = estate_id
      )
  db.session.add(repo)
  db.session.commit()
  return jsonify({
      "message": "success"
    }), 200

@api.route('/repo/', Methods=['DELETE'])
@login_required
def delete_repo():
  repo_id = request.args.get('repo_id')
  repo = Report.query.filter_by(id=repo_id).first()

  if repo is None:
    return ({
        "message": "repo doest not exist"
      }), 404

  if repo.user_is != g.current_user.id:
    return jsonify({
      "message": "no permssion to delete"
      }), 403
  db.session.delete(repo)
  db.session.commit()
  return jsonify({
    "message": "success",
    }), 200

