from pydantic import BaseModel
from typing import Literal


class Passenger(BaseModel):
    id: int
    state: Literal["in_elevator", "out_of_elevator"] = "out_of_elevator"
    current_floor: int
    destination_floor: int
    is_waiting_for_elevator: bool = True
