import logging
from datetime import datetime, timezone, timedelta
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from domain.posts.dal import PostsDAL
from utils.config import settings
import random
from domain.schedules.dal import ScheduleDAL

async def publish_post(bot: Bot, post_id: int):
    """
    Публикует один пост и помечает его как опубликованный.
    """
    logging.info(f"Attempting to publish post_id: {post_id}")
    post = PostsDAL.get_post_by_id(post_id)

    if not post:
        logging.error(f"Cannot publish post_id: {post_id}. Not found.")
        return

    if post['published_at']:
        logging.warning(f"Post_id: {post_id} has already been published at {post['published_at']}. Skipping.")
        return

    try:
        await bot.send_message(
            chat_id=settings.CHANNEL_ID,
            text=post['content_text'],
        )
        PostsDAL.mark_post_as_published(post_id)
        logging.info(f"Successfully published post_id: {post_id} to channel {settings.CHANNEL_ID}")
    except Exception as e:
        logging.error(f"Failed to send post_id: {post_id}. Error: {e}")


def schedule_bot_jobs(scheduler: AsyncIOScheduler, bot: Bot):
    """
    Планирует задачи для всех неопубликованных постов.
    """
    logging.info("Scheduling jobs for unpublished posts...")
    posts = PostsDAL.get_all_unpublished_posts()
    now = datetime.now(timezone.utc)
    
    for post in posts:
        if not post['scheduled_time']:
            continue

        # Получаем флаг random для канала
        flags = ScheduleDAL.get_schedule_settings(post['channel_id'])
        random_flag = flags.get('random', False)

        run_time = post['scheduled_time']
        if random_flag:
            delta_seconds = random.randint(-180, 180)
            run_time = run_time + timedelta(seconds=delta_seconds)

        job_id = f"post_{post['post_id']}"
        
        # Планируем только те посты, у которых время публикации в будущем
        if run_time > now:
            scheduler.add_job(
                publish_post,
                "date",
                run_date=run_time,
                kwargs={"bot": bot, "post_id": post['post_id']},
                id=job_id,
                replace_existing=True,
            )
            logging.info(f"Scheduled job for post_id: {post['post_id']} at {run_time} (random: {random_flag})")
        else:
            # Если время уже прошло, логируем и пропускаем пост
            logging.warning(f"Skipping post_id: {post['post_id']} because its scheduled time {run_time} is in the past.")


def setup_scheduler(bot: Bot):
    """
    Настраивает и запускает планировщик.
    """
    scheduler = AsyncIOScheduler(timezone="UTC")
    
    # 1. Запланировать все посты, которые есть в БД на момент старта
    schedule_bot_jobs(scheduler, bot)
    
    # 2. Периодически перепроверять БД на случай, если посты были добавлены
    #    во время работы бота. Это нужно, т.к. нет API для добавления постов.
    scheduler.add_job(
        schedule_bot_jobs,
        trigger="cron",
        minute="*/5",
        kwargs={"scheduler": scheduler, "bot": bot},
    )

    scheduler.start()
    logging.info("Scheduler started successfully.")
