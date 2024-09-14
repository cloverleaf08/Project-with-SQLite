from aiogram import Bot, Dispatcher, types, filters, F
import asyncio
from config import TOKEN, ADMIN
from database import Database  # Ensure this module is correctly implemented
from buttons.reply_btn import all_user_btn, regis_btn
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)
db = Database()  # Ensure this is initialized properly


class Registration(StatesGroup):
    first_name = State()


@dp.message(filters.Command("start"))
async def start_function(message: types.Message):
    if message.from_user.id == 5980619717:  # Adjust ID as necessary
        await message.answer("Xush kelibsiz", reply_markup=all_user_btn)
    else:
        await message.answer("Xush kelibsiz", reply_markup=regis_btn)

    db.create_table_users()  # Ensure this is async, otherwise remove await
    user_id = message.from_user.id
    user_full_name = message.from_user.full_name
    db.add_user(user_id, user_full_name)  # Ensure async


@dp.message(F.text == "Show all users")
async def get_all_users(message: types.Message):
    all_users = await db.select_user()  # Ensure this is async
    my_list = [f"ID: {user[0]} and NAME: {user[1]}" for user in all_users]
    await message.answer("\n".join(my_list))


@dp.message(F.text == "Registration")
async def first_name_function(message: types.Message, state: FSMContext):
    await message.answer("Ismingizni kiriiting🤓")
    await state.set_state(Registration.first_name)
    db.create_table_users()


@dp.message(Registration.first_name)
async def first_name_function(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    first_name = message.text
    await state.update_data(first_name=first_name)
    db.add_user(user_id, first_name)
    await message.answer("It is done")
    await state.clear()


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
