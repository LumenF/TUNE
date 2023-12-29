from apps.apps.mailing.models import SegmentationModel, SegmentBaseModel, SegmentationReadyModel, SegmentationStepModel
from apps.apps.user.models import TgUserModel
from asgiref.sync import sync_to_async


def get_1(_id):
    args = (
        'name',
        'step',
        'text',
        'to',
        'finish_id',
        'finish__name',
        'base__id',
    )
    return [i for i in SegmentationStepModel.objects.filter(
        base__id=_id,
    ).values(*args)]


async def get_quiz(_id):
    """Получить все шаги сегментации"""

    return await sync_to_async(get_1, thread_sensitive=True)(_id)


def add_user_to_segmentation(
        user: TgUserModel,
        segment: SegmentationModel
):
    user.segment.add(segment)


def set_segment(
        segmentation_name: str,
        tg_id: str,
        quiz_id: str,
):

    try:
        segment_model = SegmentationModel.objects.get(name=segmentation_name)
        user_model = TgUserModel.objects.get(tg_id=tg_id)
        quiz_model = SegmentBaseModel.objects.get(id=quiz_id)
        SegmentationReadyModel.objects.filter(
            user=user_model,
            base=quiz_model,
            segment=segment_model,

        ).delete()
        SegmentationReadyModel.objects.create(
            user=user_model,
            base=quiz_model,
            segment=segment_model,
        )
        user_model.segment.add(segment_model)
        return True
    except:
        return False


async def set_quiz_result(
        segmentation_name: str,
        tg_id: str,
        quiz_id: str,
):
    return await sync_to_async(set_segment, thread_sensitive=True)(
        segmentation_name,
        tg_id,
        quiz_id,
    )
