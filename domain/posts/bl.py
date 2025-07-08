from datetime import datetime
from domain.posts.dal import PostsDAL

class PostsBL:
    @staticmethod
    def update_post_name(post_id, name=None):
        if not name:
            return False, 'No name to update'
        success = PostsDAL.update_post_name(post_id, name)
        return success, None if success else 'Update failed'

