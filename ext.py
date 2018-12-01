from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_migrate import Migrate
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
csrf = CSRFProtect()
ckeditor = CKEditor()
moment = Moment()
migrate = Migrate()
mail = Mail()
toolbar = DebugToolbarExtension()



# current_user 获得admin对象
@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    user = Admin.query.get(int(user_id))
    return user


# 跳转用户登陆界面
login_manager.login_view = 'auth.login'
# login_manager.login_message = 'Your custom message' 设置需要登录的文字
# 消息提醒级别
login_manager.login_message_category = 'warning'


