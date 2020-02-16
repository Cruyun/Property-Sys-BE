import time
from . import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class User(UserMixin,db.Model):
  __tablename__='users'
  id=db.Column(db.Interger, primary_key=True)
  username=db.Column(db.String(20), unique=False)
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


