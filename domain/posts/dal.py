import logging
from datetime import datetime, timezone
from typing import List
from utils.connection_db import connection_db
from utils.database_manager import DatabaseManager

class PostsDAL:
    @staticmethod
    def get_all_unpublished_posts() -> list[dict]:
        from utils.database_manager import DatabaseManager
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
        from utils.database_manager import DatabaseManager
        from datetime import datetime, timezone
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
        from utils.database_manager import DatabaseManager
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
        from utils.database_manager import DatabaseManager
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

    @staticmethod
    def create_post(channel_id: int, prompt_id: int, content_name: str, content_text: str,
                    scheduled_time: datetime) -> bool:
        from utils.database_manager import DatabaseManager
        try:
            with DatabaseManager.get_cursor() as cursor:
                cursor.execute(
                    "INSERT INTO posts (channel_id, prompt_id, content_name, content_text, scheduled_time) VALUES (%s, %s, %s, %s, %s)",
                    (channel_id, prompt_id, content_name, content_text, scheduled_time)
                )
                return True
        except Exception as e:
            logging.error(f"Error creating post: {e}")
            return False

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
            import logging
            logging.error(f"Error updating post name {post_id}: {e}")
            return False