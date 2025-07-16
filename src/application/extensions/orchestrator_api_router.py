from fastapi import APIRouter


class OrchestratorAPIRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def event(self, routing_key: str): ...
