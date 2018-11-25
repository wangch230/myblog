import os
import sys
import pymysql


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.urandom(24)

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = True
    # MAIL_USE_SSL
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('机智的超', MAIL_USERNAME)
    BLOG_EMAIL = os.getenv('BLOG_EMAIL', MAIL_USERNAME)

    # 每一页的文章数
    BLOG_POST_PER_PAGE = 10
    #
    BLOG_MANAGE_POST_PER_PAGE = 15
    BLOG_COMMENT_PER_PAGE = 15
    # ('主题', '显示')
    BLOG_THEMES = {'perfect_blue': 'Perfect_Blue', 'black_swan': 'Black_Swan'}
    BLOG_SLOW_QUERY_THRESHOLD = 1


class DevelopConfig(BaseConfig):
    DB_USERNAME = 'root'
    DB_PASSWORD = 'password'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME = 'MyBlog'

    # PERMANENT_SESSION_LIFETIME =

    DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)

    SQLALCHEMY_DATABASE_URI = DB_URI


config = {
    'development': DevelopConfig
}

