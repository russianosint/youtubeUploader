from aiogram import executor

import filters
import handlers
from loader import dp

if __name__ == '__main__':
  executor.start_polling(dp)
