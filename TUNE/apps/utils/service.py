import datetime

from asgiref.sync import sync_to_async

from apps.apps.logs.models import ChapterLogs


def _up(
        chapter: str,
        button: str,
):
    result = ChapterLogs.objects.get_or_create(
        date_created=datetime.date.today(),
        chapter=chapter,
        button=button,
    )
    if not result[1]:
        result[0].increase_count()


async def update_chapter(
        chapter: str,
        button: str,
):
    await sync_to_async(
        func=_up,
        thread_sensitive=True,
    )(chapter, button)
