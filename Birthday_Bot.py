import asyncio
from datetime import datetime
from aiogram import Bot
from init_bot import dp,bot,db,scheduler
from handler import user

async def start_job():
    result = db.get_date()
    for i in result:
        await create_job(str(i[0]),datetime.strptime(i[1],'%d.%m.%Y'))

async def birthday_message(bot:Bot,db,user_id):
    result = db.get_user_subs(user_id)
    if (result[0][0]==1):
        await bot.send_message(int(user_id),"Поздравляю с днем рождения!!!")
    for i in result[0][1].split():
        await bot.send_message(int(i),f"Сегодня день рождения у {result[0][2]}. Не забудьте поздравить!")

async def create_job(user_id,date):
    scheduler.add_job(birthday_message,trigger='cron',month = int(date.month), day = int(date.day), hour = 10,args = (bot,db,user_id) )

async def main():
    await start_job()
    dp.include_router(user.router_user)    
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
