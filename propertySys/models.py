from datetime import datetime
from . import db,login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin, current_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from sqlalchemy.orm import backref, relationship
from sqlalchemy import ForeignKey
from random import seed

class User(UserMixin,db.Model):
  __tablename__='users'
  id=db.Column(db.Integer, primary_key=True)
  username=db.Column(db.String(164), default="普通住户")
  open_id = db.Column(db.String(36), index=True)  # weixin openid for identicaion
  is_admin=db.Column(db.Boolean, default=False)
  telephone=db.Column(db.String(11))
  car_no=db.Column(db.String(10))
  estate_id=db.Column(db.Integer, nullable=False) # 小区 id
  room_id=db.Column(db.Integer) # 房间 id
  parking_id=db.Column(db.Integer) # 车位 id
  #用户投诉记录
  # report_record=db.relationship('Report', backref=db.backref('user'),lazy='dynamic', cascade='all')
  #用户缴费记录
  # payment_record=db.relationship('Payment', backref=db.backref('user'), lazy='dynamic', cascade='all')

  # 生成令牌
  def generate_auth_token(self):
    s=Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'id':self.id}).decode('utf-8')
  
  # 检验令牌
  @staticmethod
  def verify_auth_token(token):
    s=Serializer(current_app.config['SECRET_KEY'])
    try:
      data=s.loads(token)
    except Exception as e:
      return None
    return User.query.get_or_404(data['id'])

  def __repr__(self):
    return "<User %r>" % self.username

  def to_resident_json(self):
    json_user = {
                'id': self.id,
                'username': self.username,
                'is_admin': self.is_admin,
                'estate_id': self.estate_id,
                'room_id': self.room_id,
                'telephone': self.telephone,
                'parking_id': self.parking_id,
                'car_no': self.car_no
                }
    return json_user

  def to_admin_json(self):
    json_user = {
                'id': self.id,
                'username': self.username,
                'is_admin': self.is_admin,
                'estate_id': self.estate_id
                }
    return json_user

# 小区
class Estate(db.Model):
  __tablename__='estates'
  id=db.Column(db.Integer, primary_key=True)
  name=db.Column(db.String(20), unique=True)

  def to_json(self):
    estate_json = {
          "id": self.id,
          "name": self.name
        }
    return estate_json

# 住房
class Room(db.Model):
  __tablename__='rooms'
  id=db.Column(db.Integer, primary_key=True)
  name=db.Column(db.String(20))
  water_used=db.Column(db.Integer, default=0)
  water_fee=db.Column(db.Integer, default=0)
  gas_used=db.Column(db.Integer, default=0)
  gas_fee=db.Column(db.Integer, default=0)
  ele_used=db.Column(db.Integer, default=0)
  ele_fee=db.Column(db.Integer, default=0)
  owner_id=db.Column(db.Integer) # 户主 id
  estate_id=db.Column(db.Integer, nullable=False) # 小区id

  def to_simple_json(self):
    room_json = {
        "id": self.id,
        "name": self.name
        }
    return room_json

  def to_detail_json(self):
    room_json = {
        "id": self.id,
        "name": self.name,
        "water_fee": self.water_fee,
        "water_used": self.water_used,
        "gas_fee": self.gas_fee,
        "gas_used": self.gas_used,
        "ele_fee": self.ele_fee,
        "ele_used": self.ele_used,
        "owner_id": self.owner_id,
        "estate_id": self.estate_id,
        "owner_id": self.owner_id
        }
    return room_json

#报告
class Report(db.Model):
  __tablename__='reports'
  id=db.Column(db.Integer, primary_key=True)
  content=db.Column(db.Text)
  state=db.Column(db.Integer, default=0) #状态 0 未处理 1 正在处理 2 已处理
  repo_type=db.Column(db.Integer, default=0) #类型 0 维修 1 投诉 2 其他
  admin_response=db.Column(db.Text)
  submit_time=db.Column(db.DateTime, default=datetime.now)
  solved_time=db.Column(db.DateTime)
  user_id=db.Column(db.Integer) # 报告人 id
  admin_id=db.Column(db.Integer) # 处理的管理员 id
  estate_id=db.Column(db.Integer, nullable=False)
  
  def to_json(self):
    json_repo = {
        'id': self.id,
        'content': self.content,
        'state': self.state,
        'repo_type': self.repo_type,
        'admin_response': self. admin_response,
        'submit_time': self.submit_time,
        'solved_time': self.solved_time,
        'user_id': self.user_id,
        'admin_id': self.admin_id,
        'estate_id': self.estate_id
        }
    return json_repo


# 通知公告
class Announcement(db.Model):
  __tablename__='announcements'
  id=db.Column(db.Integer, primary_key=True)
  content=db.Column(db.Text, nullable=False)
  title=db.Column(db.String(256), nullable=False)
  time=db.Column(db.DateTime, default=datetime.now, nullable=False)
  estate_id=db.Column(db.Integer,  nullable=False)

  def to_json(self):
    json_announce = {
      'id': self.id,
      'content': self.content,
      'title': self.title,
      'time': self.time,
      'estate_id': self.estate_id
      }
    return json_announce


# 停车场
class Parking(db.Model):
  __tablename__='parking'
  id=db.Column(db.Integer, primary_key=True)
  address=db.Column(db.String(20))
  state=db.Column(db.Integer, default=0, nullable=False) #状态 0 可停车 1 不可停车
  is_private=db.Column(db.Boolean, default=False)
  park_car_no=db.Column(db.String(10))
  owner_id=db.Column(db.Integer) # 车位主人id
  estate_id=db.Column(db.Integer,  nullable=False)
  # park_uid=db.Column(db.Integer, db.ForeignKey('users.id')) # 停车主人id
  
  def to_json(self):
    park_json = {
          "id": self.id,
          "address": self.address,
          "state": self.state,
          "is_private": self.is_private,
          "park_car": self.park_car,
          "owner_id": self.owner_id,
          "estate_id": self.estate_id
        }
    return park_json

# 缴费
class Payment(db.Model):
  __tablename__='payment'
  id=db.Column(db.Integer, primary_key=True)
  state=db.Column(db.Integer, default=0) #状态 0成功 1 失败
  type=db.Column(db.Integer, default=0) #类型 0 water 1 gas 2 ele
  amount=db.Column(db.Integer, default=0) #数量
  fee=db.Column(db.Integer, default=0) #费用
  room_id=db.Column(db.Integer, nullable=False)
  user_id=db.Column(db.Integer, nullable=False) # 缴费人id
  estate_id=db.Column(db.Integer, nullable=False)

  def to_json(self):
    json_payment = {
      'id': self.id,
      'estate_id': self.estate_id,
      'state': self.state,
      'type': self.type,
      'amount': self.amount,
      'fee': self.fee,
      'room_id': self.room_id,
      'user_id': self.user_id
      }
    return json_payment

