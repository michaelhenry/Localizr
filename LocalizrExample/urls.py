from django.urls import (path, include)
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

from apps.Localizr.views import (

	locale_list_view,
	locale_detail_view,
	app_info_list_view,
	app_info_detail_view,
	key_string_list_view,
	key_string_detail_view,
	app_info_key_string_list_view,
	app_info_key_string_detail_view,
	key_value_list_view,
	)

urlpatterns = [
    path('admin/', admin.site.urls),
]

# STATIC FILES
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('v1/token/', obtain_auth_token, name='auth-token'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('v1/locale/', locale_list_view, name='locale-list'),
    path('v1/locale/<int:pk>', locale_detail_view, name='locale-detail'),
    path('v1/app_info/', app_info_list_view, name='app-info-list'),
    path('v1/app_info/<int:pk>', locale_list_view, name='app-info-detail'),
    path('v1/key_string/', key_string_list_view, name='key-string-list'),
    path('v1/key_string/<int:pk>', key_string_detail_view, name='key-string-detail'),
    path('v1/app_info_key_string/', app_info_key_string_list_view, name='app-info-list'),
    path('v1/app_info_key_string/<int:pk>', app_info_key_string_detail_view, name='app-info-detail'),
    path('app/<slug:app_slug>-<slug:locale_code>', key_value_list_view, name='key-value-list'),
 ]
