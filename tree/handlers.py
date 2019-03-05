import json

from aiohttp import web

from tree.db import Repository
from tree.model import Leaf
from tree.exceptions import NotFoundException, BadAttribute


class Handlers:
    def __init__(self, mongo):
        self.repo = Repository(mongo)

    async def add(self, request):
        try:
            body = request.body
            leaf = Leaf(body.get('id'), body.get('name'))
            if leaf.parent_id and not await self.repo.get_one(leaf.parent_id):
                raise NotFoundException()

            await self.repo.add(leaf)
            return web.Response()
        except BadAttribute:
            return web.HTTPBadRequest()
        except NotFoundException:
            return web.HTTPForbidden()
        except Exception as e:
            print(e)
            return web.HTTPInternalServerError()

    async def get(self, request):
        q = request.query.get('q')
        id = request.query.get('id')
        branch = request.query.get('branch')
        child = request.query.get('child')

        result = []
        if q:
            result = await self.repo.search(q)
        elif branch and Leaf.is_valid_id(branch):
            result = await self.repo.get_branch(branch)
        elif id and Leaf.is_valid_id(id):
            result = await self.repo.get_one(id)
        elif child and Leaf.is_valid_id(child):
            result = await self.repo.get_children(child)
        else:
            raise web.HTTPBadRequest()
        return web.Response(text=json.dumps(result))
