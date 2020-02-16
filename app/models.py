from datetime import datetime
from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(UserMixin,db.Model):
  __tablename__='users'
  id=db.Column(db.Interger, primary_key=True)
  username=db.Column(db.String(20))
  password=db.Column(db.String(20))
  password_hash=db.Column(db.String(128))
  is_admin=db.Column(db.Boolean, default=False)
  telephone=db.Column(db.String(11), unique=True, nullable=False)
  user_type=db.Column(db.Interger, default=0) #用户类型 0 游客 1 住户
  estate_id=db.Column(db.Interger, db.ForeignKey('estates.id')) # 小区 id
  room_id=db.Column(db.Interger, db.ForeignKey('rooms.id')) # 房间 id
  parking_id=db.Column(db.Interger, db.ForeignKey('parking.id')) # 车位 id
  #用户投诉记录
  report_record=db.relationship('Report', backref=db.backref('user', lazy='joined'),lazy='dynamic')
  #用户缴费记录
  payment_record=db.relationship('Payment', backref=db.backref('user', lazy='joined'),lazy='dynamic')

  @property
  def password(self):
    raise AttributeError('password is not a readable attribute')
  
  @password.setter
  def password(self,password):
    self.password_hash=generate_password_hash(password)

  def verify_password(self,password):
    return check_password_hash(self.password_hash,password)

  # 生成令牌
  def generate_auth_token(self,expiration):
    s=Serializer(current_app.config['SECRET_KEY'],expires_in=expiration)
    return s.dumps({'id':self.id})
  # 检验令牌
  def verify_auth_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

  def __repr__(self):
    return "<User %r>" % self.username

  @login_manager.user_loader
  def load_user(user_id):
    return User.query.get(int(user_id))

# 小区
class Estate(db.Model):
  __tablename__='estates'
  id=db.Column(db.Interger, primary_key=True)
  name=db.Column(db.String(20), unique=True)
  resident_num=db.Column(db.Interger, default=0)

# 住房
class Room(db.Model):
  __tablename__='rooms'
  id=db.Column(db.Interger, primary_key=True)
  name=db.Column(db.String(20))
  water_used=db.Column(db.Interger, default=0)
  water_fee=db.Column(db.Interger, default=0)
  gas_used=db.Column(db.Interger, default=0)
  gas_fee=db.Column(db.Interger, default=0)
  ele_used=db.Column(db.Interger, default=0)
  ele_fee=db.Column(db.Interger, default=0)
  owner_id=db.Column(db.Interger, db.ForeignKey('users.id')) # 户主 id可为空
  estate_id=db.Column(db.Interger, db.ForeignKey('estates.id'), nullable=False) # 小区id

#报告
class Report(db.Model):
  __tablename__='reports'
  id=db.Column(db.Interger, primary_key=True)
  content=db.Column(db.String(255))
  state=db.Column(db.Interger, default=0) #状态 0 未处理 1 正在处理 2 已处理
  type=db.Column(db.Interger, default=0) #类型 0 维修 1 投诉 2 其他
  submit_time=db.Column(db.DateTime, default=datetime.now)
  solved_time=db.Column(db.DateTime)
  user_id=db.Column(db.Interger, db.ForeignKey('users.id')) # 报告人 id
  admin_id=db.Column(db.Interger, db.ForeignKey('users.id')) # 处理的管理员 id
  estate_id=db.Column(db.Interger, db.ForeignKey('estates.id'), nullable=False)

# 通知公告
class Announcement(db.Model):
  __tablename__='announcements'
  id=db.Column(db.Interger, primary_key=True)
  content=db.Column(db.String(1000))
  time=db.Column(db.DateTime, default=datetime.now)
  estate_id=db.Column(db.Interger, db.ForeignKey('estates.id'), nullable=False)

# 停车场
class Parking(db.Model):
  __tablename__='parking'
  id=db.Column(db.Interger, primary_key=True)
  address=db.Column(db.String(20))
  state=db.Column(db.Interger, default=0, nullable=False) #状态 0 可停车 1 不可停车
  free_start=db.Column(db.DateTime) #车位主人可修改的开放游客停车时间
  free_end=db.Column(db.DateTime)
  owner_id=db.Column(db.Interger, db.ForeignKey('users.id')) # 车位主人id
  estate_id=db.Column(db.Interger, db.ForeignKey('estates.id'), nullable=False)

# 缴费
class Payment(db.Model):
  __tablename__='payment'
  id=db.Column(db.Interger, primary_key=True)
  state=db.Column(db.Interger, default=0) #状态 0成功 1 失败
  type=db.Column(db.Interger, default=0) #类型 0 water 1 gas 2 ele
  amount=db.Column(db.Interger, default=0) #数量
  fee=db.Column(db.Interger, default=0) #费用
  room_id=db.Column(db.Interger, db.ForeignKey('rooms.id'), nullable=False)
  user_id=db.Column(db.Interger, db.ForeignKey('users.id'), nullable=False) # 缴费人id
  estate_id=db.Column(db.Interger, db.ForeignKey('estates.id'), nullable=False)
