import logging
from datetime import datetime, timezone
from typing import List
from utils.connection_db import connection_db
from utils.database_manager import DatabaseManager
from utils.database_manager import Executor
from utils.config import Settings
from .schemas import PostSchema

class PostsDAL:
    @staticmethod
    def get_all_unpublished_posts() -> list[dict]:
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "SELECT post_id, channel_id, content_name, scheduled_time, published_at FROM posts WHERE published_at IS NULL"
                )
                rows = cursor.fetchall()
                return rows if rows else []
        except Exception as e:
            logging.error(f"Error fetching unpublished posts: {e}")
            return []

    @staticmethod
    def mark_post_as_published(post_id: int) -> bool:
        try:
            with DatabaseManager.get_cursor() as cursor:
                post_published_at = datetime.now(timezone.utc)
                cursor.execute(
                    "UPDATE posts SET published_at = %s WHERE post_id = %s",
                    (post_published_at, post_id)
                )
                return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error making post {post_id} as published: {e}")
            return False

    @staticmethod
    def get_post_by_id(post_id: int) -> dict:
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "SELECT post_id, channel_id, content_name, scheduled_time, published_at FROM posts WHERE post_id = %s",
                    (post_id,)
                )
                row = cursor.fetchone()
                return row if row else None
        except Exception as e:
            logging.error(f"Error fetching post by id: {e}")
            return None

    @staticmethod
    def update_post(post_id: int, updates: dict) -> bool:
        try:
            with DatabaseManager.get_cursor() as cursor:
                set_clause = ', '.join([f"{key} = %s" for key in updates.keys()])
                values = list(updates.values())
                values.append(post_id)
                query = f"UPDATE posts SET {set_clause} WHERE post_id = %s"
                cursor.execute(query, values)
                return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error updating post {post_id}: {e}")
            return False

    # @staticmethod
    # def create_post(channel_id: int, prompt_id: int, content_name: str, content_text: str,
    #                 scheduled_time: datetime) -> bool:
    #     try:
    #         with DatabaseManager.get_cursor() as cursor:
    #             cursor.execute(
    #                 "INSERT INTO posts (channel_id, prompt_id, content_name, content_text, scheduled_time) VALUES (%s, %s, %s, %s, %s)",
    #                 (channel_id, prompt_id, content_name, content_text, scheduled_time)
    #             )
    #             return True
    #     except Exception as e:
    #         logging.error(f"Error creating post: {e}")
    #         return False

    @staticmethod
    def update_post_name(post_id, name):
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "UPDATE posts SET content_name = %s WHERE post_id = %s",
                    (name, post_id)
                )
                updated = cursor.rowcount
                return updated > 0
        except Exception as e:
            logging.error(f"Error updating post name {post_id}: {e}")
            return False

    @staticmethod
    def update_time_only_by_post_id(post_id, new_time):
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "SELECT publish_time FROM schedules WHERE post_id = %s",
                    (post_id,)
                )
                row = cursor.fetchone()
                if not row or not row['publish_time']:
                    return False
                current_publish_time = row['publish_time']
                new_publish_time = current_publish_time.replace(
                    hour=new_time.hour, minute=new_time.minute, second=0, microsecond=0
                )
                # Обновляем запись
                cursor.execute(
                    "UPDATE schedules SET publish_time = %s WHERE post_id = %s",
                    (new_publish_time, post_id)
                )
                return cursor.rowcount > 0
        except Exception as e:
            logging.error(f"Error updating only time for post_id {post_id}: {e}")
            return False

    @staticmethod
    def update_post_time_only(post_id, new_time):
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "SELECT published_at FROM posts WHERE post_id = %s",
                    (post_id,)
                )
                row = cursor.fetchone()
                if not row or not row['published_at']:
                    return False
                current_published_at = row['published_at']
                new_published_at = current_published_at.replace(
                    hour=new_time.hour, minute=new_time.minute, second=0, microsecond=0
                )
                cursor.execute(
                    "UPDATE posts SET scheduled_time = %s WHERE post_id = %s",
                    (new_published_at, post_id)
                )
                return cursor.rowcount > 0
        except Exception as e:
            import logging
            logging.error(f"Error updating only time for post_id {post_id}: {e}")
            return False

    @staticmethod
    def delete_post(post_id):
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "DELETE FROM posts WHERE post_id = %s",
                    (post_id,)
                )
                return cursor.rowcount > 0
        except Exception as e:
            import logging
            logging.error(f"Error deleting post {post_id}: {e}")
            return False

    @staticmethod
    def create_post_and_return_id(content_name, scheduled_time, channel_id, prompt_id, content_text=None, image_id=None, source_id=None):
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO posts (content_name, scheduled_time, channel_id, prompt_id, content_text, image_id, source_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING post_id
                    """,
                    (content_name, scheduled_time, channel_id, prompt_id, content_text, image_id, source_id)
                )
                row = cursor.fetchone()
                return row['post_id'] if row else None
        except Exception as e:
            import logging
            logging.error(f"Error creating post: {e}")
            return None

class NewPostDAL(Executor):
    @staticmethod
    def get_post_by_channel_id(channel_id: int) -> dict:
        try:
            query = """
                    SELECT *
                    FROM posts
                    WHERE channel_id = %s"""
            result = newPostDAL._execute_query(query=query, params=channel_id, fetchall=True)
            if result:
                result = [PostSchema(**res) for res in result]
            return result
        except:
            logging.error(f"Error fetching post by channel id: {channel_id}")
            raise


