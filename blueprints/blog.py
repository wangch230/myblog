from flask import Blueprint, request, current_app, render_template, url_for, flash, redirect, abort, make_response
from flask_login import current_user
from models import Post, Comment
from forms import AdminCommentForm
from ext import db
from utils import redirect_back


blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', posts=posts, pagination=pagination)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/post/<int:post_id>')
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLOG_POST_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(
        Comment.timestamp.asc()).paginate(page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['MAIL_USERNAME']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True

    else:
        form = Comment()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(author=author, email=email, site=site, body=body, post=post, from_admin=from_admin, reviewed=reviewed)
        replied_id = request.args.get('reply')

        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            # send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()

        if current_user.is_authenticated:
            flash('评论成功', 'success')
        else:
            flash('评论已提交，等待管理员审核', 'info')

        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)


@blog_bp.route('/change_theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookies('theme', theme_name, max_age=30 * 24 * 60 * 60)
    return response


