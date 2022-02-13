from aiogram.dispatcher.filters.state import State, StatesGroup


class YoutubeLoadState(StatesGroup):

  title = State()
  description = State()
  video = State()
  