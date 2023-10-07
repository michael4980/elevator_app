from app.models.passenger_model import Passenger
from app.misc.logger import logger
from app.elevator import Elevator
from anyio import sleep


class PassengerAction:
    def __init__(self, passenger: Passenger) -> None:
        self.passenger = passenger

    async def run_passenger_pipeline(self):
        match self.passenger.state:
            case "in_elevator":
                await Elevator().press_inner_button(self.passenger)
            case "out_of_elevator":
                await Elevator().press_outer_button(self.passenger)
        await sleep(2)
        while True:
            current_position = Elevator().current_placement
            if current_position == self.passenger.current_floor and self.passenger.state == "out_of_elevator":
                if await Elevator().has_place():
                    await self._enter_in_elevator()
                    self.passenger.state = "in_elevator"
                    self.passenger.is_waiting_for_elevator = False
                    await Elevator().press_inner_button(self.passenger)
                else:
                    logger.error(
                        f"Passenger_{self.passenger.id} can`t enter into elevator: not enough place. Waiting..."
                    )
                    await sleep(2)
            elif self.passenger.state == "in_elevator":
                if passenger := Elevator().get_passenger_by_id(self.passenger.id):
                    if passenger.destination_floor == current_position:
                        await sleep(1)
                        await self._get_out_from_elevator()
                        del Elevator().passengers[self.passenger.id]
                        return
            await sleep(2)

    async def _get_out_from_elevator(self) -> None:
        logger.info(f"Passenger_{self.passenger.id} went from elevator on {self.passenger.destination_floor}")

    async def _enter_in_elevator(self) -> None:
        logger.info(f"Passenger_{self.passenger.id} enetered into elevator on {self.passenger.current_floor}")
