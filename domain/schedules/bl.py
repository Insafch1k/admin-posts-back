from domain.schedules.dal import ScheduleDAL
from domain.schedules.schemas import ScheduleSchema

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

def format_schedule_for_frontend(schedules):
    posts = []
    for schedule in schedules:
        publish_time = schedule.publish_time
        posts.append({
            "name": f"{schedule.post_id} пост",
            "time": publish_time.strftime("%H:%M"),
            "date": publish_time.strftime("%d.%m")
        })
    return {"posts": posts}