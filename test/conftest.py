import pytest
from time import sleep
from tree.settings import config
from tree.main import init
from tree.db import Repository


@pytest.fixture
def api(loop, aiohttp_client):
    app = loop.run_until_complete(init(loop))
    drop_db_data(app)
    yield loop.run_until_complete(aiohttp_client(app))
    loop.run_until_complete(app.shutdown())


def drop_db_data(app):
    app.mongo[config.mongo_database][config.mongo_collection].delete_many({})
