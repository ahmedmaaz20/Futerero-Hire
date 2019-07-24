from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from stages import *


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AdminForm(FlaskForm):
    AdminID = StringField('AdminID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class Userprofile(FlaskForm):

    CandidateName = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    contact = IntegerField('Contact No', validators=[DataRequired()])
    NoticePeriod = StringField('Notice Period', validators=[DataRequired()])
    Skills = StringField('Skills', validators=[DataRequired()])
    Source = StringField('Source')
    #picture = FileField('Upload Resume', validators=[FileAllowed('png', 'pdf')])
    submit = SubmitField('Save')


class SearchForm(FlaskForm):
    #choices = [('Skills', 'Skills'),
               #('Job ID', 'Job ID'),
               #('Notice Period', 'Notice Period'),
               #('Status', 'Status')]
    JobID = SelectField('Select Job ID:', choices=Lookup(result4))
    Skills = StringField('')
    NoticePeriod = StringField('')
    selectR = SelectField('Select Round:', choices=Lookup(result2))
    selectS = SelectField('Select Status:', choices=Lookup(result3))
    #search = StringField('Search')
    submit = SubmitField('Search')


class Track(FlaskForm):
    selectC = SelectField('Select Candidate:', choices=Lookup(result1))
    selectJ = SelectField('Select Job ID', choices=Lookup(result4))
    selectR = SelectField('Select Round:', choices=Lookup(result2))
    selectS = SelectField('Select Status:', choices=Lookup(result3))
    submit = SubmitField('Update')