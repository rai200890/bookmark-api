import pytest
import requests
import responses
import json


def test_bookmark_list_get(api_test_client):
    response = api_test_client.get('/bookmarks?page=1&per_page=15')
    data = json.loads(response.data.decode('utf-8'))

    assert response.status_code == 200
    assert data == {
        "bookmarks": [],
        "pagination": {'has_prev': False, 'prev_page': 0, 'next_page': 2,
                       'has_next': False, 'total': 0, 'pages': 0, 'per_page': 15}
    }
