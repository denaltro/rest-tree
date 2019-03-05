from motor import motor_asyncio as ma
from pymongo import TEXT


async def setup_mongo(app, loop):
    app.mongo = ma.AsyncIOMotorClient(
        app.config.mongo_host,
        app.config.mongo_port,
        io_loop=loop
    )
    app.mongo[app.config.mongo_database][app.config.mongo_collection].create_index([
                                                                                   ('text', TEXT)])
    return app


async def close_mongo(app):
    app.mongo.close()
