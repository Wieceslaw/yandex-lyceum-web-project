import flask
from flask import render_template, redirect, request
from forms.user import RegisterForm, LoginForm
from . import db_session
from flask_restful import abort
from data.users import User
from data.themes import Themes
from data.topics import Topics
from forms.topic import TopicForm
from forms.theme import ThemeForm
from forms.message import MessageForm
from data.messages import Messages
from flask_login import login_user, login_required, logout_user, current_user

blueprint = flask.Blueprint(
    'blueprints',
    __name__,
    template_folder='templates'
)


@blueprint.route('/home')
@blueprint.route('/')
def main():
    db_sess = db_session.create_session()
    themes = db_sess.query(Themes)
    return render_template(
        'main.html',
        title='Main',
        themes=themes
    )


@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User(
            email=form.email.data,
            nickname=form.nickname.data,
            banned=False,
            moderator=False
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template(
        'register.html',
        title='Registration',
        form=form
    )


@blueprint.route('/topic/<int:id>', methods=['GET', 'POST'])
def topic(id):
    db_sess = db_session.create_session()
    topic = db_sess.query(Topics).filter(Topics.id == id).one()
    form = MessageForm()
    messages = db_sess.query(Messages).filter(Messages.topic_id == id).all()
    if request.method == 'GET':
        return render_template(
            'topic.html',
            title=topic.name,
            topic=topic,
            messages=messages,
            form=form
        )
    if request.method == 'POST':
        if form.validate_on_submit() and current_user:
            message = Messages(
                text=form.text.data,
                user_id=current_user.id,
                topic_id=id
            )
            db_sess.add(message)
            db_sess.commit()
            return redirect(f'/topic/{id}')


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect username or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint.route('/users_list')
@login_required
def users_list():
    db_sess = db_session.create_session()
    users = db_sess.query(User)
    if current_user.moderator:
        return render_template('users_list.html', title='Users', users=users)
    else:
        return abort(404)


@blueprint.route('/user_delete/<int:id>')
@login_required
def users_delete(id):
    if current_user.moderator:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).one()
        if user:
            db_sess.delete(user)
            db_sess.commit()
            return redirect('/users_list')
    return abort(404)


@blueprint.route('/user_ban/<int:id>')
@login_required
def users_ban(id):
    if current_user.moderator:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).one()
        if user:
            user.banned = True
            db_sess.commit()
            return redirect('/users_list')
    return abort(404)


@blueprint.route('/user_unban/<int:id>')
@login_required
def users_unban(id):
    if current_user.moderator:
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).one()
        if user:
            user.banned = False
            db_sess.commit()
            return redirect('/users_list')
    return abort(404)


@blueprint.route('/theme/<int:id>')
def theme(id):
    db_sess = db_session.create_session()
    theme = db_sess.query(Themes).filter(Themes.id == id).one()
    topics = db_sess.query(Topics).filter(Topics.theme_id == id).all()
    return render_template(
        'theme.html',
        title=theme.name,
        theme=theme,
        topics=topics
    )


@blueprint.route('/theme_delete/<int:id>')
@login_required
def theme_delete(id):
    if current_user.moderator:
        db_sess = db_session.create_session()
        theme = db_sess.query(Themes).filter(Themes.id == id).one()
        if theme:
            db_sess.delete(theme)
            db_sess.commit()
            return redirect('/')
    return abort(404)


@blueprint.route('/topic_delete/<int:id>')
@login_required
def topic_delete(id):
    db_sess = db_session.create_session()
    topic = db_sess.query(Topics).filter(Topics.id == id).one()
    theme_id = topic.theme_id
    if topic:
        if current_user.moderator or current_user == topic.user:
            db_sess.delete(topic)
            db_sess.commit()
            return redirect(f'/theme/{theme_id}')
    return abort(404)


@blueprint.route('/message_delete/<int:id>')
@login_required
def message_delete(id):
    db_sess = db_session.create_session()
    message = db_sess.query(Messages).filter(Messages.id == id).one()
    topic_id = message.topic_id
    if message:
        if current_user.moderator or current_user == message.user:
            db_sess.delete(message)
            db_sess.commit()
            return redirect(f'/topic/{topic_id}')
    return abort(404)


@blueprint.route('/theme_add', methods=['GET', 'POST'])
@login_required
def theme_add():
    if current_user.moderator:
        form = ThemeForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            theme = Themes(
                name=form.name.data,
                user_id=current_user.id
            )
            db_sess.add(theme)
            db_sess.commit()
            return redirect('/')
        return render_template(
            'theme_add.html',
            title='Create theme',
            form=form
        )
    return abort(404)


@blueprint.route('/topic_add/<int:theme_id>', methods=['GET', 'POST'])
@login_required
def topic_add(theme_id):
    form = TopicForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        topic = Topics(
            name=form.name.data,
            text=form.text.data,
            user_id=current_user.id,
            theme_id=theme_id
        )
        db_sess.add(topic)
        db_sess.commit()
        return redirect(f'/theme/{theme_id}')
    return render_template(
        'topic_add.html',
        title='Create topic',
        form=form,
        theme_id=theme_id
    )