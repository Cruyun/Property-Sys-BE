from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, FileField 
from wtforms.validators import Length, Required

# 发布通告表单
class PostAnnouncement(Form):
  content=TextAreaField('输入通告内容...')
  title=StringField('姓名',validators=[Length(0,51)])
  sumbit = SubmitField('提交')

# 个人资料表单
class EditProfileForm(Form):
  username=StringField('姓名',validators=[Length(0,21)])
  telephone=StringField('电话',validators=[Length(7,12)])
  car_no=StringField('车牌号',validators=[Length(0,12)])
  sumbit = SubmitField('提交')

# 提交维修或投诉
class PostReport(Form):
  content=TextAreaField('输入内容...')
  sumbit = SubmitField('提交')
