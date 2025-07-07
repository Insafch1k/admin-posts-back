from datetime import datetime
from domain.posts.dal import PostsDAL

class PostsBL:
    @staticmethod
    def update_post(post_id, name=None, date=None, time_=None):
        updates = {}
        if name:
            updates['content_name'] = name
        if date and time_:
            date_part = datetime.strptime(date, '%d.%m')
            time_part = datetime.strptime(time_, '%H:%M').time()
            updates['scheduled_time'] = datetime.combine(date_part.replace(year=datetime.now().year), time_part)
        if not updates:
            return False, 'No fields to update'
        success = PostsDAL.update_post(post_id, updates)
        return success, None if success else 'Update failed'
