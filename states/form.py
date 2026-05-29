from aiogram.fsm.state import State, StatesGroup


class ApplicationForm(StatesGroup):
    choosing_position = State()
    answering          = State()
    confirming         = State()


class AdminPanel(StatesGroup):
    searching    = State()
    writing_note = State()
