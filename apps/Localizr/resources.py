from import_export import resources
from import_export import fields

from .models import (
    Locale,
    AppInfo,
    KeyString,
    AppInfoKeyString,
    LocalizedString,
    )

from .widgets import (
    AppInfoWidget,
    LocaleWidget,
    KeyStringWidget,
    )


class AppInfoResource(resources.ModelResource):

    base_locale = fields.Field(column_name='base_locale', 
        attribute='base_locale', 
        widget=LocaleWidget(Locale, 'code'))

    class Meta:
        model = AppInfo
        import_id_fields = ['slug']
        export_order = ('name', 'slug', 'base_locale',)
        fields = ('name', 'slug', 'base_locale',)


class LocaleResource(resources.ModelResource):

    class Meta:
        model = Locale
        import_id_fields = ['code']
        export_order = ('name', 'code',)
        fields = ('name', 'code',)


class LocalizedStringResource(resources.ModelResource):

    key = fields.Field(column_name='key', 
        attribute='key_string', 
        widget=KeyStringWidget(KeyString, 'key'))

    locale = fields.Field(column_name='locale', 
        attribute='locale', 
        widget=LocaleWidget(Locale, 'code'))

    class Meta:
        model = LocalizedString
        import_id_fields = ['key', 'locale']
        export_order = ('key', 'value', 'locale')
        fields = ('key', 'value', 'locale')


class AppInfoKeyStringResource(resources.ModelResource):

    app = fields.Field(column_name='app', 
        attribute='app_info', 
        widget=AppInfoWidget(AppInfo, 'slug'))

    key = fields.Field(column_name='key', 
        attribute='key_string', 
        widget=KeyStringWidget(KeyString, 'key'))

    value = fields.Field(column_name='value', 
        attribute='value',)

    class Meta:
        model = AppInfoKeyString
        import_id_fields = ['app', 'key']
        export_order = ('key','value','app')
        fields = ('key','value', 'app',)

