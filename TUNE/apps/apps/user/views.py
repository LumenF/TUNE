import datetime

from django.shortcuts import render

from apps.apps.user.static import get_user_static_active, get_user_static_register, get_user_static_count_region

now_year = datetime.date.today().year
now_month = datetime.date.today().month


def user_active(
        request,
        year: str,
        month: str,
        city_id: str = None,
):
    if not str(year).isdigit() or str(year) == '0':
        year = now_year
    if not str(month).isdigit() or str(month) == '0':
        month = now_month
    if int(month) > 12:
        month = now_month

    context_active = get_user_static_active(
        year=year,
        month=month,
    )
    context_register = get_user_static_register(
        year=year,
        month=month,
    )
    context_user_region = get_user_static_count_region()
    return render(
        request=request,
        template_name='html/user.html',
        context=context_active | context_register | context_user_region,
    )
