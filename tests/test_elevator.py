from unittest.mock import patch, PropertyMock
import pytest


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_initialization(anyio_backend, elevator):
    assert 5 == elevator.current_placement
    assert "standing" == elevator.current_state
    assert 0 == len(elevator.passengers)


@patch("app.elevator.Elevator._Elevator__move", return_value=None)
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_add_passenger(move_patch, anyio_backend, elevator, psg1):
    await elevator.press_inner_button(psg1)
    assert 1 == len(elevator.passengers)
    elevetor_psg = elevator.get_passenger_by_id(1)
    assert elevetor_psg.current_floor == 3


@patch("app.elevator.Elevator._Elevator__move", return_value=None)
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_press_outer_button(message, anyio_backend, elevator, psg2):
    await elevator.press_outer_button(psg2)
    elevetor_psg = elevator.get_passenger_by_id(2)
    assert elevetor_psg is None


@patch("app.elevator.SendElevatorMessage.got_button_command", return_value=None)
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_choosing_direction(mock_message, anyio_backend, elevator, psg1, psg2):
    down_queue_mock = PropertyMock(return_value="moving_down")
    with patch("app.elevator.Elevator.current_state", down_queue_mock) as mock:
        await elevator.press_outer_button(psg1)
        await elevator.press_outer_button(psg2)
        assert "moving_down" == elevator.current_state
        assert elevator.floors_queue == [3, 6]
