from domain.schedules.dal import ScheduleDAL
from domain.schedules.schemas import ScheduleSchema
from collections import OrderedDict
from datetime import datetime, timedelta

class ScheduleBL:
    @staticmethod
    def get_posts_schedule_by_channel(channel_id):
        raw_posts = ScheduleDAL.get_schedules_by_channel(channel_id)
        return [
            ScheduleSchema(
                schedule_id=schedule["schedule_id"],
                channel_id=schedule["channel_id"],
                post_id=schedule["post_id"],
                publish_time=schedule["publish_time"],
                published_at=schedule["published_at"]
            )
            for schedule in raw_posts
        ]

    @staticmethod
    def duplicate_schedule_logic(channel_id, posts):
        """
        Дублирует расписание дня или недели для канала.
        posts: [{name, time, date}]
        """
        new_schedules = []
        # Определяем, дублируем день или неделю по уникальным датам
        unique_dates = set(post['date'] for post in posts)
        if len(unique_dates) == 1:
            # Дублируем день: переносим все посты на следующий день
            date_str = list(unique_dates)[0]
            old_date = datetime.strptime(date_str, '%d.%m')
            new_date = old_date + timedelta(days=1)
            for post in posts:
                time_part = datetime.strptime(post['time'], '%H:%M').time()
                new_publish_time = datetime.combine(new_date, time_part)
                new_schedules.append({
                    'channel_id': channel_id,
                    'post_id': post['name'].split()[0],
                    'publish_time': new_publish_time
                })
        else:
            # Дублируем неделю: переносим все посты на +7 дней
            for post in posts:
                old_date = datetime.strptime(post['date'], '%d.%m')
                new_date = old_date + timedelta(days=7)
                time_part = datetime.strptime(post['time'], '%H:%M').time()
                new_publish_time = datetime.combine(new_date, time_part)
                new_schedules.append({
                    'channel_id': channel_id,
                    'post_id': post['name'].split()[0],
                    'publish_time': new_publish_time
                })
        # Сохраняем новые расписания через DAL
        ScheduleDAL.insert_schedules(new_schedules)
        return {'count': len(new_schedules)}

    @staticmethod
    def get_posts_schedule_with_flags(channel_id):
        posts = ScheduleBL.get_posts_schedule_by_channel(channel_id)
        flags = ScheduleDAL.get_schedule_settings(channel_id)
        return posts, flags

    @staticmethod
    def format_schedule_for_frontend(schedules):
        posts = []
        for schedule in schedules:
            publish_time = schedule.publish_time
            posts.append(OrderedDict([
                ("post_id", schedule.post_id),  # <--- добавляем id
                ("name", f"{schedule.post_id} пост"),
                ("time", publish_time.strftime("%H:%M")),
                ("date", publish_time.strftime("%d.%m"))
            ]))
        return posts

    @staticmethod
    def save_posts_schedule_with_flags(channel_id, posts, duplication, dublicationWeek, random):
        # Удаляем старое расписание
        ScheduleDAL.delete_schedules_by_channel(channel_id)
        new_schedules = []
        for post in posts:
            date_part = datetime.strptime(post['date'], '%d.%m')
            time_part = datetime.strptime(post['time'], '%H:%M').time()
            publish_time = datetime.combine(date_part.replace(year=datetime.now().year), time_part)
            new_schedules.append({
                'channel_id': channel_id,
                'post_id': post['post_id'],
                'publish_time': publish_time
            })
        created_id = ScheduleDAL.insert_schedules(new_schedules)
        ScheduleDAL.upsert_schedule_settings(channel_id, duplication, dublicationWeek, random)
        return {'count': len(new_schedules), 'schedule_id': created_id}

    @staticmethod
    def update_schedule_time(schedule_id, publish_time):
        success = ScheduleDAL.update_schedule_time(schedule_id, publish_time)
        return success, None if success else 'Update failed'

    @staticmethod
    def create_schedule(channel_id, post_id, publish_time):
        success = ScheduleDAL.create_schedule(channel_id, post_id, publish_time)
        return success

    @staticmethod
    def delete_post_time(post_id):
        return ScheduleDAL.delete_schedules_by_post_id(post_id)

    @staticmethod
    def update_schedule_flags(channel_id, duplication, dublicationWeek, random):
        try:
            ScheduleDAL.upsert_schedule_settings(channel_id, duplication, dublicationWeek, random)
            return True
        except Exception as e:
            import logging
            logging.error(f"Error updating schedule flags: {e}")
            return False