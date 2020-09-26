from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Snap.models import User, Post
from flask_login import current_user


from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    password = PasswordField(' Password', validators=[DataRequired()])

    confirm_password = PasswordField(' Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('The username is already taken!')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('The email is already taken!')


class LoginForm(FlaskForm):

    email = StringField('Email', validators=[DataRequired(), Email()])

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])

    password = PasswordField(' Password', validators=[DataRequired()])

    remember = BooleanField(' Remember Me')

    submit = SubmitField('Login ')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('The email is already taken!')


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('content', validators=[DataRequired()])
    picture = FileField('Update Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    tag = SelectField(
        'Tag', choices=[( '😀 Happy', '😀 Happy'), ('😔 Sad', '😔 Sad'), ('😤 Angry', '😤 Angry')])
    submit = SubmitField('Post')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'The username is already taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'The email is already taken. Please choose a different one.')


class UpdateAccountForm(FlaskForm):

    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=20)])

    email = StringField('Email', validators=[DataRequired(), Email()])

    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Update')

    bio = StringField('bio', validators=[
                        Length(min=0, max=200)])
    link = StringField('Link', validators=[
                    Length(min=0, max=200)])

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('The username is already taken!')


    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('The email is already taken!')
