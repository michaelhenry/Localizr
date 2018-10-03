from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404

from .serializers import (
    LocaleSerializer, 
    AppInfoSerializer, 
    KeyStringSerializer, 
    AppInfoKeyStringSerializer,
    KeyValueSerializer,
    LocalizedStringSerializer,
    )
from .models import (
    Locale, 
    AppInfo, 
    KeyString, 
    AppInfoKeyString,
    LocalizedString,
    get_localized_strings,
    )

from rest_framework.renderers import (
    JSONRenderer,
    BrowsableAPIRenderer,
    )

from .renderers import (
    KeyStringIOSRenderer,
    KeyStringAndroidRenderer,
    ReactNativeRenderer,
    )


class LocaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Locale to be viewed or edited.
    """
    queryset         = Locale.objects.all()
    serializer_class = LocaleSerializer


class AppInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AppInfo to be viewed or edited.
    """
    queryset         = AppInfo.objects.all()
    serializer_class = AppInfoSerializer

class KeyStringViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows KeyString to be viewed or edited.
    """
    queryset         = KeyString.objects.all()
    serializer_class = KeyStringSerializer


class AppInfoKeyStringViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AppInfoKeyString to be viewed or edited.
    """
    queryset         = AppInfoKeyString.objects.all()
    serializer_class = AppInfoKeyStringSerializer


class AppInfoKeyStringViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows AppInfoKeyString to be viewed or edited.
    """
    queryset         = AppInfoKeyString.objects.all()
    serializer_class = AppInfoKeyStringSerializer


class LocalizedStringViewSet(viewsets.ModelViewSet):

    queryset         = LocalizedString.objects.all()
    serializer_class = LocalizedStringSerializer


class KeyStringLocalizedView(APIView):
    """
    API endpoint that allows to view the key-value list of an specified app and locale
    """

    renderer_classes = (
        BrowsableAPIRenderer, 
        JSONRenderer, 
        KeyStringIOSRenderer,
        KeyStringAndroidRenderer,
        ReactNativeRenderer,
        )

    def get(self, request, *args, **kwargs):

        try:
            app_slug = kwargs['app_slug']
            locale_code = kwargs.get('locale_code', 'en')
            app = AppInfo.objects.select_related().get(slug=app_slug)
            keyvalues_q = get_localized_strings(app=app, locale_code=locale_code)
            queryset = keyvalues_q.order_by('key',)

            serializer = KeyValueSerializer(queryset, many=True)
            response = Response(serializer.data)
            last_modified_q = keyvalues_q.order_by('-modified').values_list('modified')

            if last_modified_q.exists():
                x_last_modified = "%s" % (last_modified_q.first()[0].strftime("%Y-%m-%d %H:%M %Z"))
                response['X-Last-Modified'] = x_last_modified
            return response
        except AppInfo.DoesNotExist:
            raise Http404("Not exist.")


locale_list_view = LocaleViewSet.as_view({
    'get': 'list',
    'post': 'create',
    })

locale_detail_view = LocaleViewSet.as_view({
    'get'   :   'retrieve',
    'put'   :   'update',
    'patch' :   'partial_update',
    'delete':   'destroy',
    })

app_info_list_view = AppInfoViewSet.as_view({
    'get'   :   'list',
    'post'  :   'create',
    })

app_info_detail_view = AppInfoViewSet.as_view({
    'get'   :   'retrieve',
    'put'   :   'update',
    'patch' :   'partial_update',
    'delete':   'destroy',
    })


key_string_list_view = KeyStringViewSet.as_view({
    'get'   :   'list',
    'post'  :   'create',
    })

key_string_detail_view = KeyStringViewSet.as_view({
    'get'   :   'retrieve',
    'put'   :   'update',
    'patch' :   'partial_update',
    'delete':   'destroy',
    })

app_info_key_string_list_view = AppInfoKeyStringViewSet.as_view({
    'get'   :   'list',
    'post'  :   'create',
    })

app_info_key_string_detail_view = AppInfoKeyStringViewSet.as_view({
    'get'   :   'retrieve',
    'put'   :   'update',
    'patch' :   'partial_update',
    'delete':   'destroy',
    })

localized_string_list_view = LocalizedStringViewSet.as_view({
    'get'   :   'list',
    'post'  :   'create',
    })

localized_string_detail_view = LocalizedStringViewSet.as_view({
    'get'   :   'retrieve',
    'put'   :   'update',
    'patch' :   'partial_update',
    'delete':   'destroy',
    })

key_value_list_view = KeyStringLocalizedView.as_view()

