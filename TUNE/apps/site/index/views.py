import datetime

from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView


def set_cookie(
        response: HttpResponse,
        key: str,
        value: str,
        cookie_host: str,
        days_expire: int = 365,
):
    max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(days=days_expire), "%a, %d-%b-%Y %H:%M:%S GMT",
    )
    domain = cookie_host.split(":")[0]
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=domain,
        secure=False,
    )


class IndexView(TemplateView):
    template_name = 'html/site/index.html'

    def get(self, request: WSGIRequest, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        set_cookie(
            response=response,
            key="COOKIE_KEY",
            value="231323",
            cookie_host=request.get_host(),
            days_expire=7,
        )
        return response
