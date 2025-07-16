from application.data_classes.process_file_event_dc import ProcessFileEventDC
from application.enums.routing_keys import RoutingKeys
from application.handlers.file_manager_handler import FileManagerHandler


class RabbitMQHandler:
    @classmethod
    def handler_mapping(cls):
        return {
            RoutingKeys.FILE_PROCESSOR.value: cls._process_files,
            RoutingKeys.LOG_PROCESSOR.value: cls._log_event,
        }

    @staticmethod
    async def _process_files(message: dict):
        dc = ProcessFileEventDC(**message)
        await FileManagerHandler.process_files(dc.file_metadata_ids)

    @staticmethod
    async def _log_event(message: dict):
        print(message)
