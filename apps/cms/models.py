from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash


class CmsPermission(object):
    # 以255的二进制方式表示权限，1111 1111
    ALL_PERMISSION = 0b11111111
    # 1.访问者权限
    VISITOR = 0b00000001
    # 2.管理帖子的权限
    POSTER = 0b00000010
    # 3.管理评论的权限
    COMMENTER = 0b00000100
    # 4.管理板块的权限
    BOARDER = 0b00001000
    # 5.管理前台用户的权限
    FRONTUSER = 0b00010000
    # 6.管理后台用户的权限
    CMSUSER = 0b00100000
    # 7.最高权限
    ADMINER= 0b01000000


cms_role_user = db.Table(
    'cms_role_user',
    db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
    db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True)
)


class CmsUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(50),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw_password):
        self._password = generate_password_hash(raw_password)

    def check_password(self,raw_password):
        result = check_password_hash(self.password,raw_password)
        return result

    @property
    def permissions(self): # 通过这个函数，可以获取用户拥有的所有权限
        if not self.roles:
            return 0
        # 如果用户有角色，再看他具有哪些权限
        all_permissions = 0
        for role in self.roles:
            permissions = role. permissions
            all_permissions |= permissions
        return all_permissions


    def has_permission(self,permission):
        all_permissions = self.permissions
        result = all_permissions&permission == permission
        return result

    @property
    def is_develop(self):
        return self.has_permission(CmsPermission.ALL_PERMISSION)


class CmsRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name  = db.Column(db.String(50),nullable=True)
    desc = db.Column(db.String(200),nullable=True)
    permissions = db.Column(db.Integer,default=CmsPermission.VISITOR)
    create_time = db.Column(db.DateTime,default=datetime.now)

    users = db.relationship('CmsUser',secondary=cms_role_user,backref='roles')



# 密码对外的字段叫做password，对内叫做_password

