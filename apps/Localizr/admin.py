from django.contrib import admin

from import_export.admin import ImportExportModelAdmin

from .models import (
    UserInfoSavableModel,
    Locale,
    AppInfo,
    KeyString,
    AppInfoKeyString,
    LocalizedString,
    )

from .resources import (
    AppInfoResource,
    LocaleResource,
    AppInfoKeyStringResource,
    LocalizedStringResource,
    )


class UserInfoSavableAdmin(object):

    exclude = ('created_by', 'modified_by',)


class BaseModelAdmin(UserInfoSavableAdmin, admin.ModelAdmin):

    pass


class BaseTabularInlineModelAdmin(UserInfoSavableAdmin, admin.TabularInline):

    pass


class LocaleAdmin(BaseModelAdmin, ImportExportModelAdmin):

    ordering            =   ('name','code',)
    search_fields       =   ('name','code',)
    list_display        =   ('name' ,'code','description')
    resource_class      =   LocaleResource


class AppInfoAdmin(BaseModelAdmin, ImportExportModelAdmin):

    fields              =   ('name', 'slug', 'description', 'base_locale',)
    ordering            =   ('name',)
    search_fields       =   ('name','description',)
    list_display        =   ('name', 'slug', 'description', 'base_locale')
    prepopulated_fields =   {'slug':('name',)}
    resource_class      =   AppInfoResource

class LocalizedStringInline(BaseTabularInlineModelAdmin):

    model = LocalizedString
    extra = 1


class KeyStringAdmin(BaseModelAdmin):

    ordering            =    ('key',)
    search_fields       =    ('key','description',)
    list_display        =    ('key' ,'description',)
    inlines             =    [LocalizedStringInline,]

    
class AppInfoKeyStringAdmin(BaseModelAdmin, ImportExportModelAdmin):

    fields              =    ('app_info', 'key_string',)
    ordering            =    ('key_string__key', 'app_info',)
    search_fields       =    ('key_string__key',)
    list_display        =    ('key_string', 'value', 'app_info',)
    list_filter         =    ('app_info',)
    autocomplete_fields =    ['key_string', 'app_info']
    resource_class      =    AppInfoKeyStringResource


class LocalizedStringAdmin(BaseModelAdmin, ImportExportModelAdmin):

    ordering            =    ('key_string__key', 'value', 'locale',)
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