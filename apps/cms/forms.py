from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,EqualTo,InputRequired,Length
from ..forms import *
from utils import mycache
from wtforms import ValidationError
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[InputRequired("请输入邮箱"),Email(message="请输入正确的邮箱")])
    password = StringField(validators=[Length(6,20,message="请输入正确的密码")])
    remember = IntegerField()
    # remember = StringField()


class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message="请输入正确的旧密码")])
    newpwd = StringField(validators=[Length(6,20,message="请输入正确格式新密码")])
    newpwd_repeat = StringField(validators=[EqualTo('newpwd')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[InputRequired("请输入邮箱"),Email(message="请输入正确的邮箱")])
    captcha = StringField(validators=[InputRequired("请输入验证码"),Email(message="请输入合法的验证码长度"),Length(min=6,max=6)])

    # 验证验证码和缓存数据是否相等
    # 由于本地环境问题，memcached 无法安装，此处仅仅作为案例实验
    def validate_captcha(self,filed):
        captcha = filed.data
        # email = self.email
        captcha_cache = mycache.get_(self.email)
        if captcha_cache and captcha.lower() == captcha_cache.lower():
            pass
        else:
            raise ValidationError("验证码验证错误")


    # 验证不能修改相同的邮箱
    def validate_email(self,filed):
        email = filed.data
        user = g.cms_user
        if user.email == email:
            raise ValidationError("邮箱不能相同")




