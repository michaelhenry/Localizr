from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export import fields

from .models import (
    UserInfoSavableModel,
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


class UserInfoSavableAdmin(object):

    exclude = ('created_by', 'modified_by',)

    def save_model(self, request, obj, form, change):

        if not hasattr(obj, 'created_by'):
            obj.created_by = request.user
        obj.created_by = request.user
        obj.modified_by = request.user
        obj.save()

    def save_formset(self, request, form, formset, change): 
        
        objs = formset.save(commit=False)
        for obj in objs:
            if issubclass(obj.__class__, UserInfoSavableModel):
                if not hasattr(obj, 'created_by'):
                    obj.created_by = request.user
                obj.modified_by = request.user
            obj.save()


class BaseModelAdmin(UserInfoSavableAdmin, admin.ModelAdmin):

    pass


class BaseTabularInlineModelAdmin(UserInfoSavableAdmin, admin.TabularInline):

    pass


class LocaleAdmin(BaseModelAdmin):

    ordering        =   ('name','code',)
    search_fields   =   ('name','code',)
    list_display    =   ('name' ,'code','description')
    

class AppInfoAdmin(BaseModelAdmin):

    fields              =   ('name', 'slug', 'description', 'base_locale',)
    ordering            =   ('name',)
    search_fields       =   ('name','description',)
    list_display        =   ('name', 'slug', 'description', 'base_locale')
    prepopulated_fields =   {'slug':('name',)}


class LocalizedStringInline(BaseTabularInlineModelAdmin):

    model = LocalizedString
    extra = 1


class KeyStringAdmin(BaseModelAdmin):

    ordering        =    ('key',)
    search_fields   =    ('key','description',)
    list_display    =    ('key' ,'description',)
    inlines         =    [LocalizedStringInline,]

    
class AppInfoKeyStringAdmin(BaseModelAdmin, ImportExportModelAdmin):

    fields              =    ('app_info', 'key_string',)
    ordering            =    ('app_info', 'key_string',)
    search_fields       =    ('key_string__key',)
    list_display        =    ('key_string' ,'app_info',)
    list_filter         =    ('app_info',)
    autocomplete_fields =    ['key_string', 'app_info']
    resource_class      =    AppInfoKeyStringResource


class LocalizedStringAdmin(BaseModelAdmin, ImportExportModelAdmin):

    ordering            =    ('key_string', 'locale', 'value',)
    search_fields       =    ('key_string__key', 'value',)
    list_display        =    ('value', 'key_string', 'locale',)
    list_filter         =    ('locale',)
    autocomplete_fields =    ['key_string', 'locale']
    resource_class      =    LocalizedStringResource


admin.site.register(Locale, LocaleAdmin)
admin.site.register(AppInfo, AppInfoAdmin)
admin.site.register(KeyString, KeyStringAdmin)
admin.site.register(AppInfoKeyString, AppInfoKeyStringAdmin)
admin.site.register(LocalizedString, LocalizedStringAdmin)
admin.site.site_header = 'Localizr'