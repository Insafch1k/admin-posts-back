import logging
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from sqlalchemy.orm import Session, scoped_session

from domain.database import db_manager
from domain.posts.base_model import Post


def get_session() -> Optional[scoped_session]:
    """Помощник для получения нового сеанса БД"""
    db_session_factory = db_manager.get_session()
    if not db_session_factory:
        logging.error("Database session factory not available.")
        return None
    return db_session_factory()

def get_all_unpublished_posts() -> List[Post]:
    """
    Получает все посты, которые ещё не были опубликованы
    """
    session = get_session()
    if not session:
        return []
    try:
        posts = session.query(Post).filter(Post.published_at.is_(None)).all()
        for post in posts:
            session.expunge(post)
        return posts
    except Exception as e:
        logging.error(f"Error fetching unpublished posts: {e}")
        return []
    finally:
        session.close()

def mark_post_as_published(post_id: int) -> bool:
    """
    Помечает пост как опубликованный и устанавливает текущее время
    """
    session = get_session()
    if not session:
        return False
    try:
        post = session.query(Post).filter(Post.post_id == post_id).first()
        if post:
            post_published_at = datetime.now(timezone.utc)
            session.commit()
            return True
        return False
    except Exception as e:
        logging.error(f"Error making post {post_id} as published")
        session.rollback()
        return False
    finally:
        session.close()

def get_post_by_id(post_id: int) -> Optional[Post]:
    """
    Получает один пост по его ID
    """
    session = get_session()
    if not session:
        return None
    try:
        post = session.query(Post).filter(Post.post_id == post_id).first()
        if post:
            session.expunge(post)
        return post
    except Exception as e:
        logging.error(f"Error fetching post by id: {e}")
        return None
    finally:
        session.close()


