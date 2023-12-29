from datetime import datetime

from django.contrib import admin
from rangefilter.filters import DateRangeFilterBuilder, DateTimeRangeFilterBuilder, NumericRangeFilterBuilder

from apps.abstraction.admin import AbstractAdmin
from apps.apps.logs.models import CSVLogs, ProductLogs, UserLogs, AmountProductLogs, ChapterLogs, ManagerLogs, \
    BookingProductLogs


@admin.register(CSVLogs)
class CSVLogsAdmin(AbstractAdmin):
    list_display = (
        'date_created',
        'city',
    )
    list_filter = (
        'date_created',
    )


@admin.register(ProductLogs)
class ProductLogsAdmin(AbstractAdmin):
    list_display = (
        'product',
        'count',
        'date_created',
    )
    list_filter = (
        'product__status',
        'product__subcategory',
        'date_created',
    )


@admin.register(UserLogs)
class UserLogsAdmin(AbstractAdmin):
    list_display = (
        'count',
        'date_created',
    )
    list_filter = (
        'date_created',
    )


@admin.register(AmountProductLogs)
class AmountProductLogsAdmin(AbstractAdmin):
    pass


@admin.register(ChapterLogs)
class ChapterLogsAdmin(AbstractAdmin):
    list_display = (
        'date_created',
        'chapter',
        'button',
        'count',
    )

    list_filter = (
        ("date_created", DateRangeFilterBuilder()),
        # (
        #     "date_created",
        #     DateTimeRangeFilterBuilder(
        #         title="Выберите дату",
        #         default_start=datetime(2020, 1, 1),
        #         default_end=datetime(2030, 1, 1),
        #     ),
        # ),
        # ("date_created", NumericRangeFilterBuilder()),
    )


@admin.register(ManagerLogs)
class ManagerLogsAdmin(AbstractAdmin):
    list_display = (
        'date_created',
        'count',
    )


@admin.register(BookingProductLogs)
class BookingProductLogsAdmin(AbstractAdmin):
    list_display = (
        'date_created',
        'count',
    )
