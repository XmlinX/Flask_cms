from flask import session,redirect,url_for
from functools import wraps
import config


def login_require(func):

    @wraps(func)
    def inner(*args,**kwargs):
        if  config.CmsUid in session:
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return inner
