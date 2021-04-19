import sqlalchemy
import datetime
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Messages(SqlAlchemyBase):
    __tablename__ = 'messages'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    user = orm.relation('User')
    topic_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('topics.id'))
    topic = orm.relation('Topics')