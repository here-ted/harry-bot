import logging
import datetime
from turtle import pos
from typing import Set

import aiohttp
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, JobQueue, CallbackContext

import config

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 存储订阅用户的chat_id集合
subscribed_users: Set[int] = set()


async def request(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()  # 检查HTTP错误
            return await response.text()


async def post(url: str, data: dict, headers: dict) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            response.raise_for_status()  # 检查HTTP错误
            return await response.json()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # 将用户添加到订阅列表
    if chat_id not in subscribed_users:
        subscribed_users.add(chat_id)
        logger.info(f'用户 {chat_id} 已订阅每日新闻推送')
    
    # 获取并发送当前新闻
    news = await get_news()
    await context.bot.send_message(chat_id=chat_id, text=news)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


# 定时任务函数 - 向所有订阅的用户发送消息
async def scheduled_task(context: CallbackContext):
    news = await get_news()
    await push_bullet(news)

    # 向所有订阅用户发送新闻
    for chat_id in subscribed_users:
        try:
            await context.bot.send_message(
                chat_id=chat_id, 
                text=news
            )
            logger.info(f'已向用户 {chat_id} 发送每日新闻')
        except Exception as e:
            logger.error(f'向用户 {chat_id} 发送消息失败: {str(e)}')
            # 如果发送失败，可能是用户已取消关注，可以考虑从订阅列表中移除
            subscribed_users.remove(chat_id)


async def get_news() -> str:
    # 获取新闻
    news = ''
    for url in config.news_60_base_array:
        try:
            news = await request(url)
            break
        except Exception as e:
            news = str(e)
    return news


# 计算下一次执行时间（每天早上8:45）
def get_next_run_time():
    now = datetime.datetime.now()
    # 设置今天的8:45
    next_run = now.replace(hour=8, minute=45, second=0, microsecond=0)
    # 如果今天的8:45已经过了，则设置为明天的8:45
    if next_run < now:
        next_run += datetime.timedelta(days=1)
    return next_run


async def push_bullet(news: str):
    await post(config.push_bullet_push_url, 
            { 
                'type':'note',
                'title':'每日新闻' + datetime.datetime.now().strftime('%Y-%m-%d'),
                'body':'news'
            },
            {
                'Access-Token': config.push_bullet_token,
                'Content-Type': "application/json"
            }
        )


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.tg_bot_token).build()

    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)

    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)

    # 设置每天早上8:45自动执行的定时任务
    job_queue = application.job_queue
    next_run_time = get_next_run_time()
    
    # 计算距离下一次执行的秒数
    seconds_until_next_run = (next_run_time - datetime.datetime.now()).total_seconds()
    
    # 设置重复执行的定时任务（每天一次）
    job_queue.run_repeating(
        scheduled_task, 
        interval=24 * 60 * 60,  # 24小时，即每天执行一次
        first=seconds_until_next_run,  # 第一次执行的延迟时间
        name="daily_news_task"
    )
    
    logger.info(f'已设置每日新闻定时任务，下次执行时间：{next_run_time}')
    application.run_polling()
