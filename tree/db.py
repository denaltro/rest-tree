from tree.model import Leaf
from tree.settings import config


class Repository:
    def __init__(self, mongo):
        self.collection = mongo[config.mongo_database][config.mongo_collection]

    async def add(self, model):
        return await self.collection.update_one({
            '_id': model.id
        }, {
            '$set': {
                'name': model.name,
                'parent_id': model.parent_id,
                'text': model.text
            }
        }, upsert=True)

    async def get_one(self, id):
        return await self.collection.find_one({
            '_id': id
        })

    async def get_branch(self, id):
        id_parents = Leaf.get_with_parents_array(id)
        if not id_parents:
            return []
        cursor = self.collection.find({
            '_id': {
                '$in': id_parents
            }
        })
        return await cursor.to_list(length=None)

    async def get_children(self, id):
        cursor = self.collection.find({
            'parent_id': id
        })
        return await cursor.to_list(length=None)

    async def search(self, text):
        cursor = self.collection.find(
            {'$text': {
                '$search': text
            }})
        return await cursor.to_list(length=None)
