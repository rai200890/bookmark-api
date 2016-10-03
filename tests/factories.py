import factory
from factory.alchemy import SQLAlchemyModelFactory

from bookmark_api import db
from bookmark_api.models import (
    User,
    Role,
    Bookmark
)


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db.Session

    id = factory.Sequence(lambda n: n)
    username = factory.Sequence(lambda n: 'User {}'.format(n))
    email = factory.Sequence(lambda n: 'email{}@mail.com'.format(n))


class RoleFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Role
        sqlalchemy_session = db.Session

    id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: lambda n: 'Role {}'.format(n))


class BookmarkFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Bookmark
        sqlalchemy_session = db.Session

    id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: lambda n: 'Title {}'.format(n))
    url = factory.Sequence(lambda n: lambda n: 'www.website{}.com'.format(n))
