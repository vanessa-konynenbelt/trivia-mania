import this
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, Form, FormField, FieldList
from wtforms.validators import DataRequired

class questionForm(Form):
    question = TextAreaField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])

class TriviaForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])  
    questions = FieldList(FormField(questionForm), min_entries=5, max_entries=16)
    submit = SubmitField('Post')
