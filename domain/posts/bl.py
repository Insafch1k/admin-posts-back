from datetime import datetime
from domain.posts.dal import PostsDAL
from utils.check_news.is_fit_post import compare_news_with_posts
from .dal import NewPostDAL
from .schemas import PostSchema


import time


class PostsBL:
    @staticmethod
    def update_post_name(post_id, name=None):
        if not name:
            return False, 'No name to update'
        success = PostsDAL.update_post_name(post_id, name)
        return success, None if success else 'Update failed'

    @staticmethod
    def create_post(channel_id, prompt_id, content_name, content_text, date, time_):
        try:
            date_part = datetime.strptime(date, "%d.%m")
            time_part = datetime.strptime(time_, "%H:%M").time()
            scheduled_time = datetime.combine(date_part.replace(year=datetime.now().year), time_part)
        except Exception as e:
            return False

        success = PostsDAL.create_post(channel_id, prompt_id, content_name, content_text, scheduled_time)
        return success


class newPostBL:
    @staticmethod
    def find_repeat_in_posts(news_text, channel_id):
        posts = NewPostDAL.get_post_by_channel_id(channel_id)
        print(posts)
        # compare_news_with_posts(news_text, posts)


