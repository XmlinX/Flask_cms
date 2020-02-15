from flask import Blueprint,views,render_template,request,session,url_for,redirect
from .forms import LoginForm
from .models import CmsUser
from .decorators import login_require
import config


bp = Blueprint("cms",__name__,url_prefix='/cms')


@bp.route('/')
@login_require
def index():
    return render_template('cms/cms_index.html')


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
        pass


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
            errors = form.errors
            message = errors.popitem()[1][0]
            return self.get(message=message)


bp.add_url_rule('/login/',view_func=LoginView.as_view('login'))
bp.add_url_rule('/resetpwd/',view_func=ResetPwdView.as_view('resetpwd'))
