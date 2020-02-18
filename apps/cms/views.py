import string
import random
from flask import (
    Blueprint,
    views,
    render_template,
    request,
    session,
    url_for,
    redirect,
    jsonify,
    g
)
from flask_mail import Message
from .forms import LoginForm,ResetPwdForm
from .models import CmsUser
from .decorators import login_require
import config
from utils import restful
from exts import db,mail


bp = Blueprint("cms",__name__,url_prefix='/cms')


@bp.route('/')
@login_require
def index():
    return render_template('cms/cms_index.html')


class LoginView(views.MethodView):

    def get(self,message=None):
        return render_template('cms/cms_login.html',message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = request.form.get('password')  # password = request.args.get('password') 查询字符串形式采用此种方式
            remember = form.remember.data
            user = CmsUser.query.filter_by(email=email).first()
            if user and user.check_password(password):
                # session['user_id'] = user.id
                session[config.CmsUid] = user.id
                if remember:
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message="邮箱或密码输入错误")
        else:
            message = form.get_errors()
            return self.get(message=message)


@bp.route('/logout/')
@login_require
def logout():
    session.clear()
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_require
def profile():
    return render_template('cms/cms_profile.html')


class ResetPwdView(views.MethodView):
    decorators = [login_require]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        if form.validate():
            oldpwd = request.form.get('oldpwd')
            newpwd = form.newpwd.data
            user = g.cms_user
            if user.check_password(oldpwd):
                user.password = newpwd
                db.session.commit()
                # return jsonify({"code":200,"message":""})
                return restful.success()
            else:
                return restful.params_error("旧密码错误")
        else:
            return restful.params_error(form.get_errors())


@bp.route('/email_captcha/')
@login_require
def email_captcha():

    email = request.args.get('email')
    if not email:
        return restful.params_error("请输入邮箱账号")
    source = list(string.ascii_letters)
    source.extend(map(lambda x:str(x),range(0,10)))
    captcha = "".join(random.sample(source,6))

    message = Message("Python论坛邮件验证码",recipients=[email],body="你正在修改Python论坛登录邮箱账号,你的验证码是: %s"%captcha)
    try:
        mail.send(message)
    except:
        return restful.server_error()
    return restful.success()


class ResetEmailView(views.MethodView):
    decorators = [login_require]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        email = request.form.get('email')
        g.cms_user.email = email
        db.session.commit()
        return restful.success()



bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/',view_func=ResetEmailView.as_view('resetemail'))