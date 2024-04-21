from flask import blueprints, render_template, Blueprint

main = Blueprint('main',__name__)
@main.route('/')
def index():
    return render_template('')
