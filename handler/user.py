from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime as dt
from aiogram.utils.keyboard import InlineKeyboardBuilder
from init_bot import bot,db
from Birthday_Bot import create_job


class Registration(StatesGroup):
    waiting_for_date = State()
    waiting_for_subs = State()
    

def in_subs(user_id,sub_id):
    if (user_id in sub_id): 
        return "✅"
    else:
        return ""
            

builder = InlineKeyboardBuilder()
builder.add(types.InlineKeyboardButton(
        text="Да",
        callback_data="Yes"),
        types.InlineKeyboardButton(
        text="Нет",
        callback_data="No")
    )

router_user = Router()

@router_user.message(Command("start"))
async def cmd_start(message: Message,state: FSMContext):
    if (db.user_exists(str(message.from_user.id))):
        await message.answer(f"Вы уже авторизованны. Для настройки подписок напишите команду /subs.\nПосмотреть ваши подписки, напишите /view.\nПодписаться или отписаться от поздравления, напишите /congrat.")
        await message.delete()
    else:
        await message.answer(
            f"Для начала вам необходимо пройти регистрацию."
            f"Напишите дату вашего дня рождения, например 01.01.2004 :"
        )
        await message.delete()
        await state.set_state(Registration.waiting_for_date)
    
@router_user.message(Registration.waiting_for_date)
async def listing(message: Message,state: FSMContext):
    try:
        date = dt.strptime(message.text, '%d.%m.%Y')
        datenow = dt.now()
        if (date > datenow):
            await message.answer(
            "Дата введена некоректно. Вы еще не родились."
            )
        else:
            db.add_user(str(message.from_user.id),str(message.text),str(message.from_user.full_name))
            await create_job(str(message.from_user.id),date)
            await message.answer(
            "Авторизация завершена. Теперь вы можете подписаться на уведомления написав команду /subs."
            )
            await message.answer(
            "Вы хотите чтобы бот поздравлял вас?",
            reply_markup=builder.as_markup()
            )
            await state.clear()
    except:
        await message.answer(
            "Дата введена некоректно."
            )
    
@router_user.message(Command("subs","s"))
async def cmd_start(message: Message,state: FSMContext):
    await message.delete()
    if (db.user_exists(str(message.from_user.id))):
         result = db.get_users_subs(str(message.from_user.id))
         result = list(map(list,result))
         lst=""
         for i in range(len(result)):
             lst+=f"{i+1}. {result[i][1]}   {in_subs(str(message.from_user.id),result[i][2].split())}\n"
         await message.answer(
         f"Укажите на каких пользователей вы хотите быть подписаны или хотите отписаться.\n"
         f"Напишите номера нужных пользователей через пробел."
         )
         await message.answer(
         f"Список пользователей:\n\n"
         f"{lst}"
         )
         await state.set_data(result)
         await state.set_state(Registration.waiting_for_subs)    

@router_user.message(Command("view","v"))
async def cmd_start(message: Message,state: FSMContext):
    await message.delete()
    if (db.user_exists(str(message.from_user.id))):
        result = db.get_users_subs(str(message.from_user.id))
        result = list(map(list,result))
        lst=""
        for i in range(len(result)):
            if(result[i][2])==None:
                result[i][2]=""
            lst+=f"{i+1}. {result[i][1]}   {in_subs(str(message.from_user.id),result[i][2].split())}\n"
        await message.answer(
        f"Список пользователей:\n\n"
        f"{lst}"
        )

@router_user.message(Registration.waiting_for_subs)
async def listing(message: Message,state: FSMContext):
    result = await state.get_data()
    try:
        lst = message.text.split()
        for i in lst:
            subs = result[int(i)-1][2].split()
            if str(message.from_user.id) in subs:
                subs.remove(str(message.from_user.id))
                result[int(i)-1][2] = " ".join(list(subs))
            else:
                subs.append(str(message.from_user.id))
                result[int(i)-1][2] = " ".join(list(subs))
            db.update_subs(str(result[int(i)-1][0]),result[int(i)-1][2])
        await message.answer("Подписки успешно изменились!")
        await state.clear()
    except:
        await message.answer("Данные введены некоректно, попробуйте снова.")
    

@router_user.message(Command("congrat","c"))
async def cmd_start(message: Message):
    await message.delete()
    if (db.user_exists(str(message.from_user.id))):
        await message.answer(
        "Вы хотите чтобы бот поздравлял вас?",
        reply_markup=builder.as_markup()
        )

@router_user.callback_query(F.data == "Yes")
async def send_random_value(callback: types.CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
    db.agreement_yes(str(callback.from_user.id))
    
@router_user.callback_query(F.data == "No")
async def send_random_value(callback: types.CallbackQuery,state: FSMContext):
     await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
     db.agreement_no(str(callback.from_user.id))