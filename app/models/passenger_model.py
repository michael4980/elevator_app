from pydantic import BaseModel, root_validator
from typing import Literal


class Passenger(BaseModel):
    id: int
    state: Literal["in_elevator", "out_of_elevator"] = "out_of_elevator"
    current_floor: int
    destination_floor: int
    is_waiting_for_elevator: bool = True
    
    @root_validator(pre=False)
    def current_floor_not_equal_destination_floor(cls, values):
        current_floor = values.get('current_floor')
        destination_floor = values.get('destination_floor')
        if current_floor == destination_floor:
            raise ValueError("Current floor cannot be equal to destination floor")
        return values