import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from data.config import ADMIN_ID
from filters.is_admin import IsAdmin
from googleapiclient.errors import HttpError
from loader import bot, dp
from states.loadState import YoutubeLoadState
from utils.yotube_uploader import send_video


@dp.message_handler(IsAdmin(), commands='start')
async def start(message: types.Message):
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True).add(types.KeyboardButton(text='📹 Загрузить видео'))
  await message.answer('Добро пожаловать, Админ!\n\n<b>Уровень доступа установлен на ID: {}</b>\n\nВаше меню 👇👇👇'.format("".join(str(ADMIN_ID))), reply_markup=markup)

@dp.message_handler(IsAdmin(), lambda m: m.text == '📹 Загрузить видео')
async def upload_video(message: types.Message):
  markup = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text='Отменить', callback_data='cancel'))
  await message.answer('Введите название для видео, которое хотите загрузить...', reply_markup=markup)

  await YoutubeLoadState.title.set()

@dp.message_handler(IsAdmin(), state=YoutubeLoadState.title)
async def upload_video_title_set(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['title'] = message.text

  await message.answer('Введите описание...')
  
  await YoutubeLoadState.next()

@dp.message_handler(IsAdmin(), state=YoutubeLoadState.description)
async def upload_video_description_set(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    data['description'] = message.text

  await message.answer('Загрузите видео...')

  await YoutubeLoadState.next()

@dp.message_handler(IsAdmin(), content_types=["video"], state=YoutubeLoadState.video)
async def upload_video_video_set(message: types.Message, state: FSMContext):
  async with state.proxy() as data:
    title = data['title']
    description = data['description']

  await message.video.download()
  dirs = os.listdir('videos')
  try:
    send_video(title=title, description=description, video=f'videos/{dirs[-1]}')
    os.remove(path=f'videos/{dirs[-1]}')
    await message.answer('OK!')
    await state.finish()
  except HttpError:
    await message.answer('Лимит на загрузку видео исчерпан! Смените аккаунт.')
    await state.finish()


@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'cancel', state=YoutubeLoadState.title)
async def upload_video_title_cancel(callback: types.CallbackQuery, state: FSMContext):

  await state.finish()
  await callback.message.answer('Вы отменили отправку!')

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'cancel', state=YoutubeLoadState.description)
async def upload_video_description_cancel(callback: types.CallbackQuery, state: FSMContext):

  await state.finish()
  await callback.message.answer('Вы отменили отправку!')

@dp.callback_query_handler(IsAdmin(), lambda c: c.data == 'cancel', state=YoutubeLoadState.video)
async def upload_video_cancel(callback: types.CallbackQuery, state: FSMContext):

  await state.finish()
  await callback.message.answer('Вы отменили отправку!')
