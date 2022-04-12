from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import Trivia, Question
from myapp.trivia.forms import TriviaForm, QuestionForm

trivias = Blueprint('trivias', __name__)

@trivias.route('/create', methods=['GET', 'POST'])
@login_required
def create_trivia():
    triviaForm = TriviaForm()
    if triviaForm.validate_on_submit():
        trivia = Trivia(title = triviaForm.title.data, user_id=current_user.id)
        db.session.add(trivia)
        db.session.commit()
        flash('Trivia Created')
        print('Trivia was created')
        return redirect(url_for('core.index'))
    questionForm = QuestionForm()
    questionForm.trivia_id.choices = [(row.id, row.title) for row in Trivia.query.all()] #where user_id=current_user
    if questionForm.validate_on_submit():
        question = Question(question=questionForm.question.data, answer=questionForm.answer.data, trivia_id = questionForm.trivia_id.data)
        db.session.add(question)
        db.session.commit()
        flash('Question Created')
        print('Question was created')
        return redirect(url_for('core.index'))
    return render_template('create_trivia.html', triviaForm=triviaForm, questionForm=questionForm)


@trivias.route('/create', methods=['GET', 'POST'])
@login_required
def create_question():
    questionForm = QuestionForm()
    if questionForm.validate_on_submit():
        question = Question(question=questionForm.question.data, answer=questionForm.answer.data, trivia_id = questionForm.trivia_id.data)
        db.session.add(question)
        db.session.commit()
        flash('Question Created')
        print('Question was created')
        return redirect(url_for('core.index'))
    return render_template('create_trivia.html', questionForm=questionForm)

# Make sure the trivia_id is an integer!
@trivias.route('/<int:trivia_id>')
def trivia(trivia_id):
    trivia = Trivia.query.get_or_404(trivia_id) 
    return render_template('trivia.html', title=trivia.title, date=trivia.date, post=trivia)


@trivias.route('/<int:trivia_id>/update',methods=['GET','POST'])
@login_required
def update(trivia_id):
    trivia = Trivia.query.get_or_404(trivia_id)

    if trivia.author != current_user:
        abort(403)

    form = TriviaForm()

    if form.validate_on_submit():
        trivia.title = form.title.data
        # trivia.question = form.question.data
        # trivia.answer = form.answer.data
        db.session.commit()
        flash('Trivia Updated')
        return redirect(url_for('trivias.trivia',trivia_id=trivia.id))

    elif request.method == 'GET':
        form.title.data = trivia.title
        # form.question.data = trivia.question
        # form.answer.data = trivia.answer

    return render_template('create_trivia.html',title='Updating',form=form)

@trivias.route('/<int:trivia_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(trivia_id):

    trivia = Trivia.query.get_or_404(trivia_id)
    if trivia.author != current_user:
        abort(403)

    db.session.delete(trivia)
    db.session.commit()
    flash('Trivia Deleted')
    return redirect(url_for('core.index'))