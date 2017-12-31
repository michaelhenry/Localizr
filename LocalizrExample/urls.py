from django.urls import (path, include)
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

from .views import login_view
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
  localized_string_list_view,
  localized_string_detail_view,
  )

urlpatterns = [
  path('', admin.site.urls),
  path('v1/token/', obtain_auth_token, name='auth-token'),
  path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

# STATIC FILES
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# PAGES
urlpatterns += [

  path('v1/locales/', locale_list_view, name='locale-list'),
  path('v1/locales/<int:pk>', locale_detail_view, name='locale-detail'),
  path('v1/apps/', app_info_list_view, name='app-info-list'),
  path('v1/apps/<int:pk>', locale_list_view, name='app-info-detail'),
  path('v1/keys/', key_string_list_view, name='key-string-list'),
  path('v1/keys/<int:pk>', key_string_detail_view, name='key-string-detail'),
  path('v1/app-key-strings/', app_info_key_string_list_view, name='app-key-strings-list'),
  path('v1/app-key-strings/<int:pk>', app_info_key_string_detail_view, name='app-key-strings-detail'),
  path('v1/localized-strings/', localized_string_list_view, name='localized-string-list'),
  path('v1/localized-strings/<int:pk>', localized_string_detail_view, name='localized-string-detail'),
  path('app/<slug:app_slug>.<slug:locale_code>', key_value_list_view, name='key-value-list'),
  path('v1/login/', login_view, name='login'),

 ]

if settings.DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns  += [
      path('__debug__/', include(debug_toolbar.urls)),
  ]


admin.site.site_header      =    'Localizr'
admin.site.site_title       =    'Localizr'
admin.site.site_url         =     None