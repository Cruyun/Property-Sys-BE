'''
  POST  /login/   登录
'''
import requests
from . import api
from flask import request, jsonify
from ..models import User
from .. import db
#from flask import current_app as app

#wx_appid = app.config['WX_APPID']
#wx_appsecret = app.config['WX_APPSECRET']
wx_openid_url = "https://api.weixin.qq.com/sns/jscode2session"
wx_appid = "wx2a3f2162a9ff0b82"
wx_appsecret = "e69c8136e92e14b89025f6e6232d9976"

@api.route('/login/', methods=['POST'])
def login():
  code = request.get_json().get("code")
  estate_id = request.get_json().get("estate_id")

  if code is None:
    return jsonify({
      'success': False,
      'message': 'code can not be none!',
      }), 400
  if estate_id is None:
    return jsonify({
        'success': False,
        'message': 'estate_id can not be none!'
      }), 400
  payload = {'appid': wx_appid, 'secret': wx_appsecret, 'js_code': code, 'grant_type': 'authorization_code'}
  r = requests.get(wx_openid_url, params=payload)
  if r.status_code != 200:
    return jsonify({
      'success': False,
      'message': 'request status code is %s' %  r.status_code,
      }), 401

  try:
    rj = r.json()
  except Exception as e:
    return jsonify({
      'success': False,
      'message': 'response jsonify failed, ex= %s' % e.message,
      }), 401
  else:
    if rj.get('openid') is not None:
      user_id = None
      openid = rj['openid']
      user = User.query.filter_by(open_id=openid).first()
      token = ""
      message = ""
      is_admin = False
      if user is not  None:
        token = user.generate_auth_token()
        user_id = user.id
        is_admin = user.is_admin
        message = "not first login"
      else:
        # generate that user
        try:
          user = User(open_id=openid)
          user.estate_id = estate_id
          db.session.add(user)
          db.session.commit()
          token = user.generate_auth_token()
          user_id = user.id
          is_admin = user.is_admin
        except Exception as e:
          message = "failed in generating the user, ex= %s" % e.message
        else:
          message = "first login, and generate that user"
      return jsonify({
        'success': True,
        'token': token,
        'message': message,
        'id': user_id,
        'is_admin': is_admin
        }), 200
    else:
      return jsonify({
        'success': False,
        'message': 'get openid failed, error message=  %s' % rj.get('errmsg'),
        }), 401
