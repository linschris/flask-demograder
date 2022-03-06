from flask import Blueprint, render_template, url_for, request, session, redirect, abort
from werkzeug.utils import secure_filename

from .forms import UserForm
from .models import db, User, Course, Assignment, Question, QuestionFile
from .dispatch import evaluate_submission

blueprint = Blueprint(name='demograder', import_name='demograder')


def get_user():
    user_email = session.get('user_email')
    return User.query.filter(User.email == user_email).first()


def get_context():
    context = {}
    user = get_user()
    if not user:
        abort(401)
    context['user'] = user

    # FIXME temporary DB dump
    context['users'] = User.query.all()
    context['courses'] = Course.query.all()
    context['assignments'] = Assignment.query.all()
    context['questions'] = Question.query.all()
    context['question_files'] = QuestionFile.query.all()

    return context


@blueprint.route('/')
def root():
    user = get_user()
    if user:
        return redirect(url_for('demograder.home'))
    return render_template('index.html')


@blueprint.route('/home')
def home():
    context = get_context()
    return render_template('home.html', **context)


@blueprint.route('/user/<user_id>')
def user_view(user_id):
    return f'{user_id=}' # TODO


@blueprint.route('/question/<question_id>')
def question_view(question_id):
    return f'{question_id=}' # TODO


@blueprint.route('/submission/<submission_id>')
def submission_view(submission_id):
    return f'{submission_id=}' # TODO


@blueprint.route('/download_submission/<submission_id>')
def download_submission(submission_id):
    return f'{submission_id=}' # TODO


@blueprint.route('/result/<result_id>')
def result_view(result_id):
    return f'{result_id=}' # TODO


@blueprint.route('/download_result/<result_id>')
def download_result(result_id):
    return f'{result_id=}' # TODO


@blueprint.route('/file/<file>')
def file_view(file_id):
    return f'{file_id=}' # TODO


@blueprint.route('/download_file/<file>')
def download_file(file_id):
    return f'{file_id=}' # TODO


# FORMS


@blueprint.route('/forms/user/', defaults={'user_id': None}, methods=('GET', 'POST'))
@blueprint.route('/forms/user/<user_id>', methods=('GET', 'POST'))
def user_form(user_id):
    context = get_context()
    form = UserForm()
    if form.validate_on_submit():
        # if the form is being submitted, process it for data
        if form.id.data:
            # if there is an ID, this is editing an existing User
            user = User.query.filter_by(id=form.id.data).first()
            user.preferred_name = form.preferred_name.data
            user.family_name = form.family_name.data
            user.email = form.email.data
            user.admin = form.admin.data
            user.faculty = form.faculty.data
        else:
            # otherwise, this is creating a new User
            user = User(
                preferred_name=form.preferred_name.data,
                family_name=form.family_name.data,
                email=form.email.data,
                admin=form.admin.data,
                faculty=form.faculty.data,
            )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('demograder.home')) # FIXME
    elif user_id is not None:
        user = User.query.filter_by(id=user_id).first()
        form.preferred_name.default = user.preferred_name
        form.family_name.default = user.family_name
        form.email.default = user.email
        form.admin.default = user.admin
        form.faculty.default = user.faculty
    return render_template('forms/user.html', form=form, **context)


# REDIRECTS


@blueprint.errorhandler(401)
def unauthorized_error(error):
    return redirect(url_for('demograder.root'))
