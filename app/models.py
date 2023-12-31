from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_login import UserMixin
from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя (Администратора)', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Регистрация')


class LoginForm(FlaskForm):
    username = StringField('Имя пользователя (Администратора)', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Вход')


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    balance = db.Column(db.Float, default=0.0)

    user = db.relationship('User', backref='clients', foreign_keys=[user_id])


class ClientForm(FlaskForm):
    name = StringField('Имя клиента', validators=[DataRequired(), Length(min=2, max=50)])
    phone = StringField('Телефон клиента', validators=[DataRequired(), Length(min=7, max=20)])
    submit = SubmitField('Добавить в БД')


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class NoteForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired(), Length(min=2, max=50)])
    content = StringField('Содержание', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Добавить заметку')

