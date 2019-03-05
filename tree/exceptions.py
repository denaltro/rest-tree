from aiohttp import web


class NotFoundException(Exception):
    pass


class BadAttribute(Exception):
    pass
