from app.misc.logger import logger


class SendElevatorMessage:
    @staticmethod
    def moving_message(direction: str, floor: int, current: int) -> None:
        logger.info(f"Elevator moving {direction} to {floor} floor now elevator on {current} floor")

    @staticmethod
    def arriving_message(current: int) -> None:
        logger.info(f"Elevator arrived on {current} floor")

    @staticmethod
    def doors_closing() -> None:
        logger.info(f"Warning!!! doors are closing...")

    @staticmethod
    def doors_opening() -> None:
        logger.info("Elevator opening doors and waiting commands...")

    @staticmethod
    def got_button_command(floor: int) -> None:
        logger.info(f"Got command: elevator will move on {floor} floor")

    @staticmethod
    def finish_message() -> None:
        logger.info("Shut down elevator ...")
