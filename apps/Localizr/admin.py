from django.contrib import admin
from django.db.models import Q, OuterRef, Subquery
from import_export.admin import ImportExportModelAdmin

from .models import (
    UserInfoSavableModel,
    Locale,
    AppInfo,
    KeyString,
    AppInfoKeyString,
    LocalizedString,
    Snapshot,
    SnapshotFile,
    AppUser,
    AppUserGroup,
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

    def get_queryset(self, request):
        qs = super(AppInfoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        user_app_ids = AppUser.objects.filter(
            user=request.user
            ).values_list('app_info__pk', flat=True)

        group_app_ids = AppUserGroup.objects.filter(
            group_id__in=request.user.groups.values_list('id', flat=True)
            ).values_list('app_info__pk', flat=True)
        return qs.filter(Q(pk__in=group_app_ids) | Q(pk__in=user_app_ids))


class LocalizedStringInline(BaseTabularInlineModelAdmin):

    model = LocalizedString
    extra = 1


class KeyStringAdmin(BaseModelAdmin):

    ordering            =    ('key',)
    search_fields       =    ('key','description',)
    list_display        =    ('key' ,'description',)
    inlines             =    [LocalizedStringInline,]


class AppInfoKeyStringAdmin(BaseModelAdmin, ImportExportModelAdmin):


    def get_queryset(self, request):
        qs = super(AppInfoKeyStringAdmin, self).get_queryset(request)

        base_value = LocalizedString.objects.filter(
            locale=OuterRef('app_info__base_locale'),
            key_string=OuterRef('key_string'),
        ).values_list('value',flat=True)

        if request.user.is_superuser:
            return qs.annotate(value=Subquery(base_value))

        user_app_ids = AppUser.objects.filter(
            user=request.user
            ).values_list('app_info__pk', flat=True)

        group_app_ids = AppUserGroup.objects.filter(
            group_id__in=request.user.groups.values_list('id', flat=True)
            ).values_list('app_info__pk', flat=True)
        return qs.filter(Q(pk__in=group_app_ids) | Q(pk__in=user_app_ids)).annotate(value=Subquery(base_value))
        

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


class SnapshotFileInline(BaseTabularInlineModelAdmin):

    model = SnapshotFile
    extra = 1


class SnapshotAdmin(BaseModelAdmin):

    ordering            =    ('key',)
    search_fields       =    ('key','app_slug',)
    list_display        =    ('key' ,'app_slug','format','created',)
    list_filter         =    ('app_slug','format',)


class AppUserAdmin(BaseModelAdmin):

    ordering            =    ('user',)
    search_fields       =    ('app_info','user',)
    list_display        =    ('user' ,'app_info',)
    list_filter         =    ('app_info',)
    autocomplete_fields =    ['app_info', 'user']


class AppUserGroupAdmin(BaseModelAdmin):

    ordering            =    ('group',)
    search_fields       =    ('app_info','group',)
    list_display        =    ('group' ,'app_info',)
    list_filter         =    ('app_info',)
    autocomplete_fields =    ['app_info', 'group']


admin.site.register(Locale, LocaleAdmin)
admin.site.register(AppInfo, AppInfoAdmin)
admin.site.register(KeyString, KeyStringAdmin)
admin.site.register(AppInfoKeyString, AppInfoKeyStringAdmin)
admin.site.register(LocalizedString, LocalizedStringAdmin)
admin.site.register(Snapshot, SnapshotAdmin)
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(AppUserGroup, AppUserGroupAdmin)