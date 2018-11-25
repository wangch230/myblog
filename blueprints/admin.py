from flask import Blueprint, request, flash, render_template
from flask_login import login_required, current_user
from forms import SettingForm
from ext import db


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    form = SettingForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.blog_title = form.blog_title.data
        current_user.blog_sub_title = form.blog_sub_title.data
        current_user.about = form.about.data
        db.session.commit()
        flash('修改已更新', 'success')
        return render_template('')
    form.about.data = current_user.about
    form.blog_title.data = current_user.blog_title
    form.blog_sub_title.data = current_user.blog_sub_title
    form.name.data = current_user.name

