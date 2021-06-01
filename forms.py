from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators  import DataRequired, InputRequired



class ChatMessageForm(FlaskForm):
    client_name = StringField(u'Client')
    id = StringField(u'ID')
    message = StringField('Message')

class LoginForm(FlaskForm):    
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')