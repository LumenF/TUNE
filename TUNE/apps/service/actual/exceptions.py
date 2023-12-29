from django.contrib import messages
from django.utils.safestring import mark_safe

from apps.service.typing import PriceDict


def raise_exception(self, data: PriceDict,):
    message = get_exception_data(self, data.values, data.status_code)
    self.admin.message_user(
        self.request,
        message=message,
        level=messages.ERROR
    )
    return None


def get_exception_data(self, values, status: str):
    line = values['line'].encode('utf-8')
    if status == '1101':
        return mark_safe(
            'Ошибка актуализации! <br>'
            'Статус 1101<br><br>'
            f'Прайс: {self.price.category.name}<br>'
            f'Строка: {values["line"]}<br>'
            f'Причина: ключ "{values["type_error"]}" не определен! <br><br><br>'
            f'Подробнее: <a href="https://docs.google.com/document/d/1u35QbEsn3hj_rKBz2f6vHUb1X-N9fTf0YmsSrbNoZQw/edit#heading=h.hdwvgrgquetn">Открыть</a>'
        )
    if status == '1102':
        return mark_safe(
            'Ошибка актуализации! <br>'
            'Статус 1102<br><br>'
            f'Прайс: {self.price.category.name}<br>'
            f'Строка: {values["line"]}<br>'
            f'Причина: ключ "{values["type_error"]}" не определен!  <br><br>'
            f'Подробнее: <a href="https://docs.google.com/document/d/1u35QbEsn3hj_rKBz2f6vHUb1X-N9fTf0YmsSrbNoZQw/edit#heading=h.aley5knkdbom">Открыть</a>'
        )
