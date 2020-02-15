from flask import session,g
from .models import CmsUser
from .views import bp
import config



# 定义钩子函数
@bp.before_request
def before_request():
    if config.CmsUid in session:
        uid = session.get(config.CmsUid)
        user = CmsUser.query.get(uid)
        if user:
            g.cms_user = user
    else:
        pass