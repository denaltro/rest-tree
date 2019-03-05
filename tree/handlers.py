import json

from aiohttp import web
from tree.db import Repository
from tree.model import Leaf


class Handlers:
    def __init__(self, mongo):
        self.repo = Repository(mongo)

    async def add(self, request):
        body = await request.json()
        if not body['id'] or not body['name']:
            raise web.HTTPBadRequest()

        leaf = Leaf(body['id'], body['name'])
        if leaf.parent_id and not await self.repo.get_one(leaf.parent_id):
            raise web.HTTPForbidden()

        await self.repo.add(leaf)
        return web.Response()

    async def get(self, request):
        q = request.query.get('q')
        id = request.query.get('id')
        branch = request.query.get('branch')
        child = request.query.get('child')

        result = []
        if q:
            result = await self.repo.search(q)
        elif branch:
            result = await self.repo.get_branch(branch)
        elif id:
            result = await self.repo.get_one(id)
        elif child:
            result = await self.repo.get_children(child)
        else:
            raise web.HTTPBadRequest()
        return web.Response(text=json.dumps(result))
