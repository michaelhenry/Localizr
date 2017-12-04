from rest_framework import viewsets
from rest_framework.generics import ListAPIView

from django.http import Http404

from .serializers import (
    LocaleSerializer, 
    AppInfoSerializer, 
    KeyStringSerializer, 
    AppInfoKeyStringSerializer,
    KeyValueSerializer,
    )
from .models import (
    Locale, 
    AppInfo, 
    KeyString, 
    AppInfoKeyString,
    LocalizedString,
    )

from rest_framework.renderers import (
    JSONRenderer,
    BrowsableAPIRenderer,
    )

from .renderers import (
    KeyStringIOSRenderer,
    KeyStringAndroidRenderer,
    )


class LocaleViewSets(viewsets.ModelViewSet):
    """
    API endpoint that allows Locale to be viewed or edited.
    """
    queryset         = Locale.objects.all()
    serializer_class = LocaleSerializer


class AppInfoViewSets(viewsets.ModelViewSet):
    """
    API endpoint that allows AppInfo to be viewed or edited.
    """
    queryset         = AppInfo.objects.all()
    serializer_class = AppInfoSerializer

class KeyStringViewSets(viewsets.ModelViewSet):
    """
    API endpoint that allows KeyString to be viewed or edited.
    """
    queryset         = KeyString.objects.all()
    serializer_class = KeyStringSerializer


class AppInfoKeyStringViewSets(viewsets.ModelViewSet):
    """
    API endpoint that allows AppInfoKeyString to be viewed or edited.
    """
    queryset         = AppInfoKeyString.objects.all()
    serializer_class = AppInfoKeyStringSerializer


class KeyStringLocalizedView(ListAPIView):
    """
    API endpoint that allows to view the key-value list of an specified app and locale
    """

    serializer_class = KeyValueSerializer
    renderer_classes = (
        BrowsableAPIRenderer, 
        JSONRenderer, 
        KeyStringIOSRenderer,
        KeyStringAndroidRenderer,
        )

    def get_queryset(self):

        app = None
        app_slug = self.kwargs['app_slug']
        locale_code = self.kwargs['locale_code']

        try:
            app = AppInfo.objects.select_related().get(slug=app_slug)
        except AppInfo.DoesNotExist:
            raise Http404("App does not exist.") 
        return AppInfoKeyString.objects\
            .filter(app_info=app)\
            .filter_by_locale_code(locale_code=locale_code)\
            .order_by('key')


locale_list_view = LocaleViewSets.as_view({
    'get': 'list',
    'post': 'create',
    })

locale_detail_view = LocaleViewSets.as_view({
    'get'   :   'retrieve',
    'put'   :   'update',
    'patch' :   'partial_update',
    'delete':   'destroy',
    })

app_info_list_view = AppInfoViewSets.as_view({
    'get'   :   'list',
    'post'  :   'create',
    })

app_info_detail_view = AppInfoViewSets.as_view({
    'get'   :   'retrieve',
    'put'   :   'update',
    'patch' :   'partial_update',
    'delete':   'destroy',
    })


key_string_list_view = KeyStringViewSets.as_view({
    'get'   :   'list',
    'post'  :   'create',
    })

key_string_detail_view = KeyStringViewSets.as_view({
    'get'   :   'retrieve',
    'put'   :   'update',
    'patch' :   'partial_update',
    'delete':   'destroy',
    })

app_info_key_string_list_view = AppInfoKeyStringViewSets.as_view({
    'get'   :   'list',
    'post'  :   'create',
    })

app_info_key_string_detail_view = AppInfoKeyStringViewSets.as_view({
    'get'   :   'retrieve',
    'put'   :   'update',
    'patch' :   'partial_update',
    'delete':   'destroy',
    })

key_value_list_view = KeyStringLocalizedView.as_view()

