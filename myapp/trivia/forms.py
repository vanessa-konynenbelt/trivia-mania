from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired

class TriviaForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    submit = SubmitField('Post')

class QuestionForm(FlaskForm):
    question = TextAreaField('Question', validators=[DataRequired()])
    answer = StringField('Answer', validators=[DataRequired()])
    trivia_id = SelectField('Trivia', validators=[DataRequired()], choices=[])
    submit = SubmitField('Post')