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
    AppInfoKeyString
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

        try:
            app = AppInfo.objects.select_related().get(slug=app_slug)
        except AppInfo.DoesNotExist:
            raise Http404("App does not exist.") 

        locale_code = self.kwargs['locale_code']

        all_key_strings = AppInfoKeyString.objects.filter(
            app_info__slug=app_slug,
        )

        localized_strings_query = all_key_strings.filter(
            key_string__values__locale__code=locale_code
        ).values(
            'key_string__key',
            'key_string__values__value'
        ).order_by('key_string__key')

        if app.base_locale:
            
            # just create a new queryset to avoid evaluation of the localized_string_query
            localized_ids_query = all_key_strings.filter(
                key_string__values__locale__code=locale_code
            ).values_list(
                'key_string__pk',
                flat=True
            )

            # then check for missing ones by excluding the found ones
            missing_strings_query = all_key_strings.filter(
                key_string__values__locale__code=app.base_locale.code
            ).exclude(key_string__pk__in=localized_ids_query).values(
                'key_string__key',
                'key_string__values__value'
            )

            localized_strings_query = localized_strings_query | missing_strings_query

        return localized_strings_query.order_by('key_string__key')


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

