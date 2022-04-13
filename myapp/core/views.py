from flask import render_template, request, Blueprint
from myapp.models import Trivia

core = Blueprint('core', __name__)

@core.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    trivias = Trivia.query.order_by(Trivia.date.desc()).paginate(page=page, per_page=5)
    # sets=[]
    # for trivia in trivias:
    #     if trivia not in sets: 
    #         sets.append(trivia)
    # print(sets)
    return render_template('index.html', trivias=trivias)

@core.route('/info')
def info():
    return render_template('info.html')