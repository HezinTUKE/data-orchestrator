from application.enums.routing_keys import RoutingKeys


class RabbitMQHandler:
    @classmethod
    def handler_mapping(cls):
        return {
            RoutingKeys.FILE_PROCESSOR.value: cls._process_files,
            RoutingKeys.LOG_PROCESSOR.value: cls._log_event
        }

    @staticmethod
    def _process_files(message: dict):
        print(message)

    @staticmethod
    def _log_event(message: dict):
        print(message)