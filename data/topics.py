import sqlalchemy
import datetime
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Topics(SqlAlchemyBase):
    __tablename__ = 'topics'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    user = orm.relation('User')

    theme_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('themes.id'))
    theme = orm.relation('Themes')
    messages = orm.relation('Messages', back_populates='topic')