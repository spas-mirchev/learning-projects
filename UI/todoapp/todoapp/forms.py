from email.policy import default
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField, BooleanField, SubmitField, SelectField
from wtforms.validators import  Length, Email, ValidationError,InputRequired
from todoapp.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()]) 
    submit = SubmitField('Sign Up') 
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class TicketForm(FlaskForm):
    name = StringField('Ticket name',validators=[InputRequired()]) 
    label = SelectField('Labels', choices=[('#FFCACA','White'),('#A10035', 'Red'), ('#372948', 'Blue'), ('#628E90', 'Green')] , default='#FBFACD')
    status = SelectField('Status', choices=[('todo', 'To do'), ('doing', 'Doing'), ('done', 'Done')],default="todo" ) 
    comment = StringField('Write a comment') 
       
    

class NewTicketForm(FlaskForm):
    name = StringField('Name of ticket', validators=[InputRequired('Please enter a name of the ticket')]) 
    status = HiddenField('Status')
   

class NewCommentForm(FlaskForm):
    name = StringField('Comment', validators=[InputRequired()]) 
    
    
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired('Oppa'), Email()])
    password = PasswordField('Password', validators=[InputRequired('Oppala')]) 
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')    