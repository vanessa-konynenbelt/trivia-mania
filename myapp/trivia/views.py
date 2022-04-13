from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import Trivia 
from myapp.trivia.forms import TriviaForm 

trivias = Blueprint('trivias', __name__)

@trivias.route('/create', methods=['GET', 'POST'])
@login_required
def create_trivia():
    triviaForm = TriviaForm()
    if triviaForm.validate_on_submit():
        for qanda in triviaForm.QandA:
            print('++++++++++++++++++++++++++++++++')
            print(qanda.data['question'])
            print(qanda.data['answer'])
            print(triviaForm.title.data)
            print(current_user.id)
            trivia = Trivia(question=qanda.data['question'], answer=qanda.data['answer'], title = triviaForm.title.data, user_id=current_user.id)
            print(trivia.question)
            print(trivia.answer)
            print(trivia.title)
            print(trivia.user_id)
            print('++++++++++++++++++++++++++++++++')
            db.session.add(trivia)
            db.session.commit()
        flash('Trivia Created')
        print('Trivia was created')
        return redirect(url_for('core.index'))
    return render_template('create_trivia.html', triviaForm=triviaForm)

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
        db.session.commit()
        flash('Trivia Updated')
        return redirect(url_for('trivias.trivia',trivia_id=trivia.id))

    elif request.method == 'GET':
        form.title.data = trivia.title

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