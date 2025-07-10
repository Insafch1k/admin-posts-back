from datetime import datetime
from domain.posts.dal import PostsDAL
from utils.check_news.is_fit_post import compare_news_with_posts
from .dal import NewPostDAL
from .schemas import PostSchema


import time


class PostsBL:
    @staticmethod
    def update_post_name(post_id, contetn_name=None):
        if not contetn_name:
            return False, 'No name to update'
        success = PostsDAL.update_post_name(post_id, contetn_name)
        return success, None if success else 'Update failed'

    # @staticmethod
    # def create_post(channel_id, prompt_id, content_name, content_text, date, time_):
    #     try:
    #         date_part = datetime.strptime(date, "%d.%m")
    #         time_part = datetime.strptime(time_, "%H:%M").time()
    #         scheduled_time = datetime.combine(date_part.replace(year=datetime.now().year), time_part)
    #     except Exception as e:
    #         return False
    #
    #     success = PostsDAL.create_post(channel_id, prompt_id, content_name, content_text, scheduled_time)
    #     return success

    @staticmethod
    def update_time_by_post_id(post_id, time_):
        from domain.schedules.dal import ScheduleDAL
        from domain.posts.dal import PostsDAL
        from datetime import time as dtime
        try:
            hour, minute = map(int, time_.split(":"))
            new_time = dtime(hour=hour, minute=minute)
            success_schedule = PostsDAL.update_time_only_by_post_id(post_id, new_time)
            success_post = PostsDAL.update_post_time_only(post_id, new_time)
            success = success_schedule and success_post
            return success, None if success else 'Update failed'
        except Exception as e:
            return False, str(e)

    @staticmethod
    def delete_post(post_id):
        return PostsDAL.delete_post(post_id)

    @staticmethod
    def create_post_and_return_id(content_name, content_text, date, time_, channel_id, prompt_id, image_id=None, source_id=None):
        from datetime import datetime
        try:
            # Собираем дату и время в один datetime
            date_part = datetime.strptime(date, "%d.%m")
            time_part = datetime.strptime(time_, "%H:%M").time()
            scheduled_time = datetime.combine(date_part.replace(year=datetime.now().year), time_part)
        except Exception as e:
            return None

        # Передаём все поля в DAL (можно добавить другие по необходимости)
        return PostsDAL.create_post_and_return_id(
            content_name=content_name,
            content_text=content_text,
            scheduled_time=scheduled_time,
            channel_id=channel_id,
            prompt_id=prompt_id,
            image_id=image_id,
            source_id=source_id
        )

class newPostBL:
    @staticmethod
    def find_repeat_in_posts(news_text, channel_id):
        posts = NewPostDAL.get_post_by_channel_id(channel_id)
        print(posts)
        # compare_news_with_posts(news_text, posts)


