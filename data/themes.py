import sqlalchemy
import datetime
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Themes(SqlAlchemyBase):
    __tablename__ = 'themes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey('users.id'))
    user = orm.relation('User')
    topics = orm.relation('Topics', back_populates='theme')