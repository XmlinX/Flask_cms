from wtforms import Form,StringField,IntegerField
from wtforms.validators import Email,EqualTo,InputRequired,Length


class LoginForm(Form):
    email = StringField(validators=[InputRequired("请输入邮箱"),Email(message="请输入正确的邮箱")])
    password = StringField(validators=[Length(6,20,message="请输入正确的密码")])
    remember = IntegerField()
    # remember = StringField()
