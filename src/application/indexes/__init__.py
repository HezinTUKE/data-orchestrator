from operator import index

from elasticsearch import Elasticsearch, helpers

from application.config import get_config_section


class BaseIndex:
    config = get_config_section("elastic")

    index = ""
    __mapping__ = {}

    @classmethod
    async def get_client(cls) -> Elasticsearch:
        return Elasticsearch(cls.config.get("url"))

    @classmethod
    async def create_index(cls):
        client = await cls.get_client()
        client.indices.create(index=cls.index, mappings=cls.__mapping__)

    @classmethod
    async def delete_index(cls):
        client = await cls.get_client()
        client.indices.delete(index=cls.index, ignore_unavailable=False)

    @classmethod
    async def bulk_create(cls, actions):
        client = await cls.get_client()
        helpers.bulk(client=client, actions=actions, index=cls.index)
