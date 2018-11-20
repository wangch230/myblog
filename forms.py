from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, ValidationError, TextAreaField,\
    HiddenField
from wtforms.validators import Length, URL, DataRequired, Email, Optional
from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from models import Category


class LoginForm(FlaskForm):

    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 20)])
    remember = BooleanField('remember me')
    submit = SubmitField('Log in ')


class SettingForm(FlaskForm):

    name = StringField('Name', validators=[DataRequired(), Length(1, 20)])
    blog_title = StringField('Blog Title', validators=[DataRequired(), Length(1, 25)])
    blog_sub_title = StringField('Blog Sub Title', validators=[DataRequired(), Length(1, 50)])
    about = CKEditorField('About Page', validators=[Length(1, 200)])
    submit = SubmitField()


class PostForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired(), Length(1, 20)])
    category = SelectField('Category', coerce=int, default=1)
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField()

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(category.name).all()]


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[Length(1, 5)])
    submit = SubmitField()

    def validate_name(self, field):
        if Category.query.filter(field.data).first():
            raise ValidationError('该目录已存在')


class CommentForm(FlaskForm):
    author = StringField('Name', validators=[Length(1, 10), DataRequired()])
    email = StringField('Email', validators=[Email(), DataRequired(), Length(1, 30)])
    site = StringField('Site', validators=[URL(), Optional(), Length(0, 50)])
    body = TextAreaField('Body', validators=[Length(1, 100), DataRequired()])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(1, 30)])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField()