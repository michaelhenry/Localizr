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

    class Meta:
        model = AppInfoKeyString
        import_id_fields = ['app', 'key']
        export_order = ('key','app')
        fields = ('key', 'app',)

