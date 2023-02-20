from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve

from ninja_extra import NinjaExtraAPI

from AVIATOR.auth_api import GlobalAuth
from user.views import router_user

api = NinjaExtraAPI(
    title='API',
    version='0.1',
    description='API Панели управления',
    app_name='Панель управления',
    csrf=False,
    auth=GlobalAuth()
)

api.add_router('/user/', router_user)

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),
    path('api/', api.urls),
    path('', admin.site.urls),
]


admin.site.site_header = 'Панель управления'
admin.site.site_title = 'Панель управления'
admin.site.index_title = ''
