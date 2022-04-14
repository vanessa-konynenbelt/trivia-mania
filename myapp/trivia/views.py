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
        for qanda in triviaForm.Question:
            trivia = Trivia(question=qanda.data['question'], answer=qanda.data['answer'], title = triviaForm.title.data, user_id=current_user.id)
            db.session.add(trivia)
            db.session.commit()
        flash('Trivia Created')
        print('Trivia was created')
        return redirect(url_for('core.index'))
    return render_template('create_trivia.html', triviaForm=triviaForm)

@trivias.route('/trivia/<string:title>', methods=['GET'])
def trivia(title):
    trivias = Trivia.query.filter_by(title=title).all()  
    return render_template('trivia.html', title=title, trivias=trivias)


@trivias.route('/delete/<string:title>',methods=['GET','POST'])
@login_required
def delete_post(title):

    trivias = Trivia.query.filter_by(title=title).all() 
    # TODO case: different users create sets with the same name
    if trivias[0].author != current_user:
        abort(403)
    for trivia in trivias:
        db.session.delete(trivia)
    
    db.session.commit()
    flash('Trivia Deleted')
    return redirect(url_for('core.index'))