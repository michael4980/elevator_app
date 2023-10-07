import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.elevator import Elevator
from app.models.passenger_model import Passenger
import pytest


@pytest.fixture
async def elevator():
    yield Elevator(capacity=7, floors_amount=20, position=5)


@pytest.fixture
async def psg1():
    yield Passenger(id=1, current_floor=3, destination_floor=8)


@pytest.fixture
async def psg2():
    yield Passenger(id=2, current_floor=6, destination_floor=9)
