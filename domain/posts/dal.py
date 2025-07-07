import logging
from datetime import datetime, timezone
from typing import List
from utils.connection_db import connection_db

class PostsDAL:
    def get_all_unpublished_posts() -> List[dict]:
        """
        Получает все посты, которые ещё не были опубликованы
        """
        conn = None
        try:
            conn = connection_db()
            cur = conn.cursor()
            cur.execute("SELECT post_id, channel_id, content_text, scheduled_time, published_at FROM posts WHERE published_at IS NULL")
            rows = cur.fetchall()
            posts = []
            for row in rows:
                posts.append({
                    "post_id": row[0],
                    "channel_id": row[1],
                    "content_text": row[2],
                    "scheduled_time": row[3],
                    "published_at": row[4]
                })
            cur.close()
            return posts
        except Exception as e:
            logging.error(f"Error fetching unpublished posts: {e}")
            return []
        finally:
            if conn:
                conn.close()

    def mark_post_as_published(post_id: int) -> bool:
        """
        Помечает пост как опубликованный и устанавливает текущее время
        """
        conn = None
        try:
            conn = connection_db()
            cur = conn.cursor()
            post_published_at = datetime.now(timezone.utc)
            cur.execute(
                "UPDATE posts SET published_at = %s WHERE post_id = %s",
                (post_published_at, post_id)
            )
            conn.commit()
            cur.close()
            return True
        except Exception as e:
            logging.error(f"Error making post {post_id} as published: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()

    def get_post_by_id(post_id: int) -> dict:
        """
        Получает один пост по его ID
        """
        conn = None
        try:
            conn = connection_db()
            cur = conn.cursor()
            cur.execute(
                "SELECT post_id, channel_id, content_text, scheduled_time, published_at FROM posts WHERE post_id = %s",
                (post_id,))
            row = cur.fetchone()
            cur.close()
            if row:
                return {
                    "post_id": row[0],
                    "channel_id": row[1],
                    "content_text": row[2],
                    "scheduled_time": row[3],
                    "published_at": row[4]
                }
            return None
        except Exception as e:
            logging.error(f"Error fetching post by id: {e}")
            return None
        finally:
            if conn:
                conn.close()