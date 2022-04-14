from flask import render_template, request, Blueprint
from myapp.models import Trivia

core = Blueprint('core', __name__)

@core.route('/trivia')
def index():
    trivias = Trivia.query.order_by(Trivia.date.desc())
    titles=[]
    for trivia in trivias:
        if trivia.title not in titles: 
            titles.append(trivia.title)
    print(titles)
    return render_template('index.html', titles=titles)

@core.route('/info')
def info():
    return render_template('info.html')