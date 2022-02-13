from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import ADMIN_ID


class IsAdmin(BoundFilter):

  async def check(self, message: types.Message):
    if message.from_user.id in ADMIN_ID:
      return True
