from tree.handlers import Handlers


def setup_routes(app):
    handlers = Handlers(app.mongo)

    app.router.add_put('/', handlers.add)
    app.router.add_get('/', handlers.get)
