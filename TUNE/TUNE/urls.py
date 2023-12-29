from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include
from django.views.static import serve
from django.conf.urls.static import static

from ninja_extra import NinjaExtraAPI

from ninja.security import HttpBearer

from apps.apps.configs.geography.api import router_invited
from apps.apps.logs.api import router_logs
from apps.apps.mailing.api import router_mail, router_segmentation
from apps.apps.product.api import router_product, router_product_new
from apps.apps.product.api_favotite import router_favorite
from apps.apps.user.api import router_user


class GlobalAuth(HttpBearer):
    def authenticate(self, request, token):
        if token == "1":
            return token


api = NinjaExtraAPI(
    title='API',
    version='0.1',
    description='API Панели управления',
    app_name='Панель управления',
    csrf=False,
    auth=GlobalAuth()

)
api.add_router('/User/', router_user)
api.add_router('/Product/', router_product)
api.add_router('/NewProduct/', router_product_new)

api.add_router('/Favorite/', router_favorite)
api.add_router('/Invited/', router_invited)

api.add_router('/Mail/', router_mail)
api.add_router('/Quiz/', router_segmentation)

api.add_router('/Logs/', router_logs)


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    path('api/', api.urls),
    # path('statistic/', include('apps.abstraction.urls')),
    path('abstraction/', include('apps.abstraction.urls')),
    path('statistic/user/', include('apps.apps.user.urls')),
    path('statistic/product/', include('apps.apps.product.urls')),
    path('csv/', include('apps.apps.configs.parameter.urls')),
    path('demo/', include('apps.site.index.urls')),
    path('demo/catalog/', include('apps.site.site_product.urls')),
    path('', admin.site.urls),

]
handler500 = 'TUNE.views.server_error'
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'ТЮН'
admin.site.site_title = 'ТЮН'
admin.site.index_title = ''
