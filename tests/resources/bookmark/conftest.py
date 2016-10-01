import json

import pytest

from bookmark_api import db
from bookmark_api.models import Bookmark


@pytest.fixture
def bookmark():
    bookmark = Bookmark(url="http://google.com", title="Google")
    db.session.add(bookmark)
    db.session.flush()
    return bookmark


@pytest.fixture
def other_bookmark():
    bookmark = Bookmark(url="http://google.com", title="Search")
    db.session.add(bookmark)
    db.session.flush()
    return bookmark
