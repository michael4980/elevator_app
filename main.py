from app.elevator import Elevator
from anyio import create_task_group, sleep
from asyncio import get_event_loop
from app.passenger import PassengerAction
from app.models.passenger_model import Passenger

psg1 = Passenger(id=1, current_floor=7, destination_floor=3)
psg2 = Passenger(id=2, current_floor=1, destination_floor=8)
psg3 = Passenger(id=3, current_floor=2, destination_floor=5)
psg4 = Passenger(id=4, current_floor=2, destination_floor=9)
psg5 = Passenger(id=5, current_floor=3, destination_floor=9)
psg6 = Passenger(id=6, current_floor=5, destination_floor=2)

psg_list = [psg1, psg2, psg3, psg4, psg5]

async def main():
    el = Elevator()
    async with create_task_group() as tg:
        tg.start_soon(el.start_elevator_pipeline)
        for psg in psg_list:
            tg.start_soon(PassengerAction(psg).run_passenger_pipeline)
        await sleep(20)
        tg.start_soon(PassengerAction(psg6).run_passenger_pipeline)
        await sleep(100)
        tg.start_soon(el.end_elevator_pipeline)
        

if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(main())