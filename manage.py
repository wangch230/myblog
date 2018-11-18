from flask_script import Manager
from flask_migrate import MigrateCommand, Migrate
from models import Admin, Category, Comment, Post, Link
from faker import Faker
from sqlalchemy.exc import IntegrityError
from random import randint

from ext import db
from app import app


fake = Faker('zh-CN')
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)


def fake_admin():
    admin = Admin(
        username='wangch30',
        blog_title='江湖人称蛋总',
        blog_subtitle='敬畏技术，谦卑而行',
        name='王',
        about='ssssss'
    )
    admin.set_password('password')
    db.session.add(admin)
    db.session.commit()


def fake_category(count=10):
    category = Category(name='python')
    db.session.add(category)
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def fake_post(count=50):
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            timestamp=fake.date_time_this_year(),
            category=Category.query.get(randint(1, Category.query.count))
        )
        db.session.add(post)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()


def fake_comment(count=500):
    #普通评论
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(randint(1, Post.query.count()))
        )

        db.session.add(comment)

    #admin
    for i in range(count/10):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            from_admin=True,
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)

    #reply
    for i in range(count/10):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            reviewed=True,
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(randint(1, Post.query.count())),
            replied=Comment.query.get(randint(Comment.query.count()))
        )
        db.session.add(comment)

    #unreviewed
    for i in range(count/10):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            post=Post.query.get(randint(1, Post.query.count()))
        )
        db.session.add(comment)


def fake_link():
    baidu = Link(name='Twitter', url='#')
    taobao = Link(name='Facebook', url='#')
    QQ = Link(name='LinkedIn', url='#')
    LOL = Link(name='Google+', url='#')
    db.session.add_all([baidu, taobao, QQ, LOL])
    db.session.commit()


@manage.command
def forge():
    fake_admin()
    print('admin is ok')
    fake_category()
    print('category is ok')
    fake_post()
    print('post is ok')
    fake_comment()
    print('commit is ok')
    fake_link()
    print('link is ok')
