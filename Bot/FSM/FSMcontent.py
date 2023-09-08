from aiogram.fsm.state import StatesGroup, State


class AlertStates(StatesGroup):
    name = State()
    surname = State()
    nickname = State()

    # cmd = State()
