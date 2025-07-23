from application.enums.elastic_inedexes import ElasticIndexes
from application.indexes import BaseIndex


class TaxiIndex(BaseIndex):
    index = ElasticIndexes.TAXI_INDEX.value

    __mapping__ = {
        "properties": {
            "metadata_id": {
                "type": "keyword",
            },
            "trip_type": {
                "type": "keyword",
            },
            "vendor_id": {
                "type": "byte",
            },
            "tpep_pickup_datetime": {
                "type": "date",
                "format": "strict_date_optional_time||epoch_second",
            },
            "tpep_dropoff_datetime": {
                "type": "date",
                "format": "strict_date_optional_time||epoch_second",
            },
            "passenger_count": {"type": "short"},
            "trip_distance": {"type": "float"},
            "rate_code_id": {
                "type": "byte",
            },
            "store_and_fwd_flag": {"type": "keyword"},
            "pu_location_id": {"type": "integer"},
            "do_location_id": {"type": "integer"},
            "payment_type": {"type": "byte"},
            "fare_amount": {"type": "float"},
            "extra": {"type": "float"},
            "mta_tax": {"type": "float"},
            "tip_amount": {"type": "float"},
            "tolls_amount": {"type": "float"},
            "improvement_surcharge": {"type": "float"},
            "total_amount": {"type": "float"},
            "congestion_surcharge": {"type": "float"},
            "airport_fee": {"type": "float"},
            "cbd_congestion_fee": {"type": "float"},
        }
    }
