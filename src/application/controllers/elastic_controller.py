import asyncio

from fastapi import APIRouter

from application.enums.elastic_inedexes import ElasticIndexes
from application.indexes.taxi_index import TaxiIndex


class ElasticController:

    name = "elastic"
    router = APIRouter(tags=[name])

    INDEX_MAPPER = {ElasticIndexes.TAXI_INDEX: TaxiIndex}

    @staticmethod
    @router.post(path=f"/{name}/create-index")
    async def create_index(index: ElasticIndexes):
        try:
            index = ElasticController.INDEX_MAPPER.get(index)
            asyncio.create_task(index.create_index())
            return {"result": True}
        except Exception as ex:
            return {"result": False}

    @staticmethod
    @router.delete(path=f"/{name}/delete-index")
    async def delete_index(index: ElasticIndexes):
        try:
            index = ElasticController.INDEX_MAPPER.get(index)
            asyncio.create_task(index.delete_index())
            return {"result": True}
        except Exception as ex:
            return {"result": False}

    @staticmethod
    @router.delete(path=f"/{name}/delete-records")
    async def delete_all_documents(index: ElasticIndexes):
        try:
            _index = ElasticController.INDEX_MAPPER.get(index)
            client = await _index.get_client()
            client.delete_by_query(index=index.value, body={"query": {"match_all": {}}})
            return {"result": True}
        except Exception as ex:
            print(ex)
            return {"result": False}
