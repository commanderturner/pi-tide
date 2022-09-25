from typing import TypedDict
from typing_extensions import NotRequired
class TideDatum(TypedDict):
    date: str
    low_1_time: NotRequired[str]
    low_1_height_m: NotRequired[float]
    low_2_time: NotRequired[str]
    low_2_height_m: NotRequired[float]
    high_1_time: NotRequired[str]
    high_1_height_m: NotRequired[float]
    high_2_time: NotRequired[str]
    high_2_height_m: NotRequired[float]
    sunset: str
    