from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from app import create_apps
from exts import db
from apps.cms import models as cms_models


CmsUser = cms_models.CmsUser
CmsRole = cms_models.CmsRole
CmsPermission = cms_models.CmsPermission


app = create_apps()
manager = Manager(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username,password,email):
    user = CmsUser(username=username,password=password,email=email)
    db.session.add(user)
    db.session.commit()
    print("cms管理用户添加成功")


@manager.command
def create_cms_role():
    # 访问者
    visitor = CmsRole(name="访问者",desc="只能查看相关数据，不能修改",permissions=CmsPermission.VISITOR)
    # 运营者
    operator = CmsRole(name="运营者",desc="管理帖子，管理评论，管理前台用户",permissions=(
        CmsPermission.VISITOR|CmsPermission.POSTER|CmsPermission.CMSUSER|CmsPermission.COMMENTER|
    CmsPermission.FRONTUSER))
    # 产品经理
    productor = CmsRole(name="管理员", desc="拥有本系统所有权限", permissions=(
            CmsPermission.VISITOR | CmsPermission.POSTER | CmsPermission.CMSUSER | CmsPermission.COMMENTER |
            CmsPermission.FRONTUSER|CmsPermission.BOARDER))
    # 开发者
    developer = CmsRole(name="开发者", desc="开发者专用角色", permissions=CmsPermission.ALL_PERMISSION)

    db.session.add_all([visitor,operator,productor,developer])
    db.session.commit()
    print("cms角色添加成功")

@manager.option("-e","--email",dest="email")
@manager.option("-n","--name",dest="name")
def add_user_to_role(email,name):
    user = CmsUser.query.filter_by(email=email).first()
    if user:
        role = CmsRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print("用户添加角色成功")
        else:
            print("没有这个角色:%s" %role)
    else:
        print("%s该用户不存在" %email)

@manager.command
def test_permission():
    user = CmsUser.query.first()
    if user.has_permission(CmsPermission.VISITOR):
        print("")
    else:
        print("")


if __name__ == '__main__':
    manager.run()