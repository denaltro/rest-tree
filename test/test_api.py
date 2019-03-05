import json
from time import sleep


async def test_add_leaf(api):
    data = {
        'id': '1',
        'name': 'test add'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(data), headers=headers)
    assert resp.status == 200


async def test_add_leaf_none_id(api):
    data = {
        'id': None,
        'name': 'test add'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(data), headers=headers)
    assert resp.status == 400


async def test_add_leaf_no_id(api):
    data = {
        'name': 'test add'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(data), headers=headers)
    assert resp.status == 400


async def test_add_leaf_no_parent(api):
    data = {
        'id': '6.6',
        'name': 'test add'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(data), headers=headers)
    assert resp.status == 403


async def test_leaf_parent_and_child(api):
    parent = {
        'id': '2',
        'name': 'test add parent'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(parent), headers=headers)
    assert resp.status == 200

    child = {
        'id': '2.2',
        'name': 'test add child'
    }
    resp = await api.put('/', data=json.dumps(child), headers=headers)
    assert resp.status == 200


async def test_add_bad_id(api):
    data = {
        'id': 'f',
        'name': 'test bad id'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(data), headers=headers)
    assert resp.status == 400


async def test_get_id(api):
    data = {
        'id': '6',
        'name': 'test bad id'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(data), headers=headers)

    resp = await api.get('/?id=6', headers=headers)
    text = await resp.text()
    assert resp.status == 200
    assert data['name'] in text
    assert data['id'] in text


async def test_get_search(api):
    data_seven = {
        'id': '7',
        'name': 'search'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(data_seven), headers=headers)

    data_eight = {
        'id': '8',
        'name': 'search'
    }
    resp = await api.put('/', data=json.dumps(data_eight), headers=headers)

    resp = await api.get('/?q=search', headers=headers)
    text = await resp.text()
    body = json.loads(text)
    assert resp.status == 200

    assert len(body) == 2
    assert data_seven['id'] in text
    assert data_seven['name'] in text
    assert data_eight['id'] in text
    assert data_eight['name'] in text


async def test_get_branch(api):
    data_seven = {
        'id': '7',
        'name': 'text search'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(data_seven), headers=headers)

    data_eight = {
        'id': '7.1',
        'name': 'text search'
    }
    resp = await api.put('/', data=json.dumps(data_eight), headers=headers)

    resp = await api.get('/?branch=7.1', headers=headers)
    text = await resp.text()
    body = json.loads(text)
    assert resp.status == 200

    assert len(body) == 2
    assert data_seven['id'] in text
    assert data_seven['name'] in text
    assert data_eight['id'] in text
    assert data_eight['name'] in text


async def test_get_child(api):
    data_seven = {
        'id': '7',
        'name': 'text search'
    }
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.put('/', data=json.dumps(data_seven), headers=headers)

    data_eight = {
        'id': '7.1',
        'name': 'text search'
    }
    resp = await api.put('/', data=json.dumps(data_eight), headers=headers)

    resp = await api.get('/?child=7', headers=headers)
    text = await resp.text()
    body = json.loads(text)
    assert resp.status == 200

    assert len(body) == 2
    assert data_seven['id'] in text
    assert data_seven['name'] in text
    assert data_eight['id'] in text
    assert data_eight['name'] in text


async def test_get_empty(api):
    headers = {
        'Authorization': api.app.config.basic_auth
    }
    resp = await api.get('/', headers=headers)
    assert resp.status == 400
