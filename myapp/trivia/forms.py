import this
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, Form, FieldList, FormField
from wtforms.validators import DataRequired

class questionForm(Form):
   question = TextAreaField('Q')
   answer = StringField('A')
 
class TriviaForm(FlaskForm):
   title = StringField('Title', validators=[DataRequired()]) 
   QandA = FieldList(FormField(questionForm), min_entries=6)
   submit = SubmitField('Post')
