import datetime
import uuid
from typing import Any

from pydantic import BaseModel, Field

from application.enums.elastic_inedexes import ElasticIndexes
from application.enums.trip_types import TripTypes


class TripDataDC(BaseModel):
    metadata_id: str = ""
    index: str = Field(ElasticIndexes.TAXI_INDEX.value, alias="_index")
    trip_type: TripTypes | None = None
    vendor_id: int = Field(0, alias="VendorID")
    tpep_pickup_datetime: int = 0
    tpep_dropoff_datetime: int = 0
    passenger_count: int = 0
    trip_distance: float = 0.0
    rate_code_id: int = Field(0, alias="RatecodeID")
    store_and_fwd_flag: str = ""
    pu_location_id: int = Field(0, alias="PULocationID")
    do_location_id: int = Field(0, alias="DOLocationID")
    payment_type: int = (0,)
    fare_amount: float = 0.0
    extra: float = 0.0
    mta_tax: float = 0.0
    tip_amount: float = 0.0
    tolls_amount: float = 0.0
    improvement_surcharge: float = 0.0
    total_amount: float = 0.0
    congestion_surcharge: float = 0.0
    airport_fee: float = 0.0
    cbd_congestion_fee: float = 0.0
