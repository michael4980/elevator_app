from typing import Literal
from app.misc.logger import logger
from app.misc.helpers import SendElevatorMessage
from anyio import sleep
from app.models.passenger_model import Passenger
from app.misc.singleton import Singleton


class Elevator(metaclass=Singleton):
    def __init__(self, capacity: int = 5, floors_amount: int = 10, position: int = 1) -> None:
        self.passengers: dict[Passenger] = {}
        self.__capacity = capacity  # max 5 people in lift
        self.__floors_amount = floors_amount
        self.__queue = []
        self.__up_queue = []
        self.__down_queue = []
        self.__current_state: Literal["moving_up", "moving_down", "standing"] = "standing"
        self.__position = position
        self.__is_working = True

    async def has_place(self) -> bool:
        if len(self.passengers) < self.__capacity:
            return True
        return False

    async def press_inner_button(self, passenger: Passenger) -> None:
        if self.passengers.get(passenger.id):
            raise ValueError("Got error you provided passenger with the same id")
        self.passengers[passenger.id] = passenger
        await self.__move(passenger.destination_floor)

    async def press_outer_button(self, passenger: Passenger) -> None:
        await self.__move(passenger.current_floor)

    async def start_elevator_pipeline(self) -> None:
        while self.__is_working:
            if self.__queue:
                await self.__add_floor_to_queue()
            if self.__up_queue or self.__down_queue:
                await self.__elevetor_moving()
            await sleep(1)
        return

    async def end_elevator_pipeline(self) -> None:
        self.__is_working = False
        self.__current_state = "standing"
        SendElevatorMessage.finish_message()

    async def __elevetor_moving(self) -> None:
        match self.__current_state:
            case "moving_up":
                if self.__up_queue:
                    return await self.__elevetor_moving_up()
                self.__current_state = "moving_down"
                return await self.__elevetor_moving()

            case "moving_down":
                if self.__down_queue:
                    return await self.__elevator_moving_down()
                self.__current_state = "moving_up"
                return await self.__elevetor_moving()

    async def __elevetor_moving_up(self) -> None:
        if self.__up_queue[0] == self.__position:
            self.__up_queue.pop(0)
            await self.__elevator_ariving_process(self.__position)
        else:
            next_floor = self.__up_queue[0]
            SendElevatorMessage.moving_message("up", next_floor, self.__position)
            await sleep(3)
            self.__position += 1

    async def __elevator_moving_down(self) -> None:
        if self.__down_queue[0] == self.__position:
            self.__down_queue.pop(0)
            await self.__elevator_ariving_process(self.__position)
        else:
            next_floor = self.__down_queue[0]
            SendElevatorMessage.moving_message("down", next_floor, self.__position)
            await sleep(3)
            self.__position -= 1

    async def __elevator_ariving_process(self, current: int) -> None:
        SendElevatorMessage.arriving_message(current)
        SendElevatorMessage.doors_opening()
        await sleep(5)
        SendElevatorMessage.doors_closing()

    async def __move(self, floor: int) -> None:
        if floor > self.__floors_amount or floor < 1:
            logger.error(f" Elevator doesn`t have that floor u can choose from 1 to {self.__floors_amount}")
            return None
        self.__queue.append(floor)
        SendElevatorMessage.got_button_command(floor)

    async def __add_floor_to_queue(self) -> None:
        match self.__current_state:
            case "moving_up":
                await self.__extend_and_sort_queue()
            case "moving_down":
                await self.__extend_and_sort_queue()
            case "standing":
                await self.__choose_direction()

    async def __extend_and_sort_queue(self) -> None:
        while self.__queue:
            floor = self.__queue.pop(0)
            if floor >= self.__position:
                self.__up_queue.append(floor)
                self.__up_queue = await self.__filter_duplicates(self.__up_queue)
                self.__up_queue.sort()
            else:
                self.__down_queue.append(floor)
                self.__down_queue = await self.__filter_duplicates(self.__down_queue)
                self.__down_queue.sort(reverse=True)

    async def __filter_duplicates(self, queue: list) -> list:
        unique_queue = set(queue)
        return list(unique_queue)

    async def __choose_direction(self):
        next_floor = self.__queue[0]
        if next_floor < self.__position:
            self.__current_state = "moving_down"
            await self.__extend_and_sort_queue()
        elif next_floor > self.__position:
            self.__current_state = "moving_up"
            await self.__extend_and_sort_queue()
        else:
            self.__queue.pop(0)
            SendElevatorMessage.doors_opening()
            await sleep(5)
            SendElevatorMessage.doors_closing()

    @property
    def current_placement(self) -> int:
        return self.__position

    @property
    def current_state(self) -> int:
        return self.__current_state

    @property
    def floors_queue(self) -> int:
        return self.__queue

    def get_passenger_by_id(self, id: int) -> Passenger | None:
        return self.passengers.get(id)
