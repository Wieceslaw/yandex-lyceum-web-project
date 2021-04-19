from flask import Flask
from flask_restful import Api
from data import db_session
from flask_login import LoginManager
from data import blueprints
from data.users import User
from data.messages import Messages
from data.topics import Topics
import os

app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


@app.template_filter('find_messages')
def find_messages(topic_id):
    db_sess = db_session.create_session()
    messages = db_sess.query(Messages).filter(Messages.topic_id == topic_id).all()
    return messages


@app.template_filter('find_topics')
def find_topics(theme_id):
    db_sess = db_session.create_session()
    topics = db_sess.query(Topics).filter(Topics.theme_id == theme_id).all()
    return topics


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if user.banned:
        return None
    else:
        return user


def main():
    db_session.global_init('db/main.db')
    app.register_blueprint(blueprints.blueprint)
    # app.run(port=8080, host='127.0.0.1')
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()