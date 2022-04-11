from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import Trivia
from myapp.trivia.forms import TriviaForm

trivias = Blueprint('trivias', __name__)

@trivias.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = Form()
    if form.validate_on_submit():
        trivia = Trivia(title=form.title.data, text=form.text.data, user_id=current_user.id)
        db.session.add(trivia)
        db.session.commit()
        flash('Trivia Created')
        print('Trivia was created')
        return redirect(url_for('core.index'))
    return render_template('create_post.html', form=form)

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
        trivia.text = form.text.data
        db.session.commit()
        flash('Trivia Updated')
        return redirect(url_for('trivias.trivia',trivia_id=trivia.id))

    elif request.method == 'GET':
        form.title.data = trivia.title
        form.text.data = trivia.text

    return render_template('create_post.html',title='Updating',form=form)

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