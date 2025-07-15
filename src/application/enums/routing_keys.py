from enum import Enum


class RoutingKeys(Enum):
    LOG_PROCESSOR = "#"
    FILE_PROCESSOR = "*.process.data"

    @staticmethod
    def get_all_processors():
        return [processor.value for processor in RoutingKeys]
