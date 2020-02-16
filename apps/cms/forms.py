from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,EqualTo,InputRequired,Length
from ..forms import *


class LoginForm(BaseForm):
    email = StringField(validators=[InputRequired("请输入邮箱"),Email(message="请输入正确的邮箱")])
    password = StringField(validators=[Length(6,20,message="请输入正确的密码")])
    remember = IntegerField()
    # remember = StringField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message="请输入正确的旧密码")])
    newpwd = StringField(validators=[Length(6,20,message="请输入正确格式新密码")])
    newpwd_repeat = StringField(validators=[EqualTo('newpwd')])