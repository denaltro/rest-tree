import base64
from aiohttp import web
from aiohttp.web import middleware


@middleware
async def check_auth(request, handler):
    auth = request.headers.get('Authorization')
    if auth == request.app.config.basic_auth:
        response = await handler(request)
        return response
    raise web.HTTPUnauthorized()
