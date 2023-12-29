import datetime
from django.shortcuts import render

from apps.apps.logs.models import AmountProductLogs
from apps.apps.product.static import get_context_category, get_context_product, get_context_product_amount, \
    get_context_product_amount_sale, get_context_product_amount_not_sale, get_context_product_favorite


def product_static(
        request,
        year: str,
        month: str,
        category_id: int = None,
):
    now_year = datetime.date.today().year
    now_month = datetime.date.today().month
    if not str(year).isdigit() or str(year) == '0':
        year = now_year
    if not str(month).isdigit() or str(month) == '0':
        month = now_month
    if int(month) > 12:
        month = now_month

    context_category = get_context_category()
    context_product = get_context_product(
        year=year,
        month=month,
        category_id=category_id,
    )

    return render(
        request=request,
        template_name='html/product.html',
        context=context_category | context_product
    )


def summ_product_static(
        request,
        year: str,
        month: str,
):
    now_year = datetime.date.today().year
    now_month = datetime.date.today().month
    if not str(year).isdigit() or str(year) == '0':
        year = now_year
    if not str(month).isdigit() or str(month) == '0':
        month = now_month
    if int(month) > 12:
        month = now_month

    context_product_amount = get_context_product_amount()
    context_product_amount_sale = get_context_product_amount_sale(
        year=year,
        month=month,
    )
    context_product_amount_not_sale = get_context_product_amount_not_sale()
    return render(
        request=request,
        template_name='html/summ.html',
        context=context_product_amount | context_product_amount_sale | context_product_amount_not_sale,
    )


def category_static(
        request,
        year: str,
        month: str,
):
    now_year = datetime.date.today().year
    now_month = datetime.date.today().month
    if not str(year).isdigit() or str(year) == '0':
        year = now_year
    if not str(month).isdigit() or str(month) == '0':
        month = now_month
    if int(month) > 12:
        month = now_month

    context_product_favorite = get_context_product_favorite()

    return render(
        request=request,
        template_name='html/views.html',
        context=context_product_favorite
    )