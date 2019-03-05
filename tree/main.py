import asyncio
from aiohttp import web
from tree.utils import setup_mongo, close_mongo
from tree.routes import setup_routes
from tree.middlewares import check_auth
from tree.settings import config


async def init(loop):
    app = web.Application(loop=loop, middlewares=[check_auth])
    app.config = config
    await setup_mongo(app, loop)
    app.on_cleanup.append(close_mongo)
    setup_routes(app)
    return app


def run():
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(init(loop))
    web.run_app(app)
