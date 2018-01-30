from django.contrib import admin
from django.db.models import (
  Q, 
  OuterRef, 
  Subquery,
)
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
from import_export.admin import ImportExportModelAdmin


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
    user_app_ids = AppInfo.objects.user_app_ids_query(request.user)
    return qs.filter(pk__in=user_app_ids)


class LocalizedStringInline(BaseTabularInlineModelAdmin):

  model = LocalizedString
  extra = 1


class KeyStringAdmin(BaseModelAdmin):

  ordering            =    ('key',)
  search_fields       =    ('key','description',)
  list_display        =    ('key' ,'description',)
  inlines             =    [LocalizedStringInline,]
  readonly_fields     =    ('modified_by', 'modified', 'created_by', 'created',)

  fieldsets = (
    ('KeyString', {
      'fields': ('key', 'description',)
    }),
    ('Metadata (Read-only)', {
      'fields': ('created_by', 'created', 'modified_by', 'modified',)
    }),
  )

  def save_model(self, request, obj, form, change):

    super(KeyStringAdmin, self).save_model(request, obj, form, change)

    if change:
      obj.modified_by = request.user
    else:
      obj.created_by = request.user
    obj.save()
    
    for v in obj.values.all():
      if not v.created_by:
        v.created_by = request.user
      else:
        v.modified_by = request.user
      v.save()


class AppInfoKeyStringListFilter(admin.SimpleListFilter):

  title = "Apps"
  parameter_name = "app_info"

  def lookups(self, request, model_admin):
    user_app_ids = AppInfo.objects.user_app_ids_query(request.user)
    q = AppInfo.objects.filter(pk__in=user_app_ids)
    return q.order_by('name').values_list('id','name')

  def queryset(self, request, queryset):

    if self.value():
      return queryset.filter(app_info__pk=self.value())
    else:
      user_app_ids = AppInfo.objects.user_app_ids_query(request.user)
      return queryset.filter(app_info__pk__in=user_app_ids)


class AppInfoKeyStringAdmin(BaseModelAdmin, ImportExportModelAdmin):

  fields              =    ('app_info', 'key_string',)
  ordering            =    ('key_string__key', 'app_info',)
  search_fields       =    ('key_string__key',)
  list_display        =    ('key_string', 'value', 'app_info',)
  list_filter         =    (AppInfoKeyStringListFilter, )
  autocomplete_fields =    ['key_string', 'app_info']
  resource_class      =    AppInfoKeyStringResource

  def get_queryset(self, request):
    qs = super(AppInfoKeyStringAdmin, self).get_queryset(request)

    base_value = LocalizedString.objects.filter(
      locale=OuterRef('app_info__base_locale'),
      key_string=OuterRef('key_string'),
    ).values_list('value',flat=True)

    if request.user.is_superuser:
      return qs.annotate(value=Subquery(base_value))

    user_app_ids = AppInfo.objects.user_app_ids_query(request.user)

    return qs.filter(
      app_info__pk__in=user_app_ids
    ).annotate(value=Subquery(base_value))
        
  

class AppLocalizedStringListFilter(admin.SimpleListFilter):

  title = "Apps"
  parameter_name = "app_info"

  def lookups(self, request, model_admin):
    user_app_ids = AppInfo.objects.user_app_ids_query(request.user)
    q = AppInfo.objects.filter(pk__in=user_app_ids)
    return q.order_by('name').values_list('id','name')

  def queryset(self, request, queryset):

    if self.value():
      keystring_ids = AppInfoKeyString.objects.filter(
        app_info__pk=self.value()).values_list('key_string__pk', flat=True)
      return queryset.filter(key_string__pk__in=keystring_ids)
    else:
      user_app_ids = AppInfo.objects.user_app_ids_query(request.user)
      keystring_ids = AppInfoKeyString.objects.filter(
        app_info__pk__in=user_app_ids).values_list('key_string__pk', flat=True)
      return queryset.filter(key_string__pk__in=keystring_ids)


class LocalizedStringAdmin(BaseModelAdmin, ImportExportModelAdmin):

  
  ordering            =    ('key_string__key', 'value', 'locale',)
  search_fields       =    ('key_string__key', 'value',)
  list_display        =    ('value', 'key_string', 'locale', 'status', )
  list_filter         =    ('locale', AppLocalizedStringListFilter, 'status',)
  autocomplete_fields =    ['key_string', 'locale']
  resource_class      =    LocalizedStringResource
  readonly_fields     =    ('modified_by', 'modified', 'created_by', 'created',)

  fieldsets = (
    ('LocalizedString', {
      'fields': ('key_string', 'locale', 'value',)
    }),
    ('Metadata (Read-only)', {
      'fields': ('created_by', 'created', 'modified_by', 'modified',)
    }),
  )

  def get_queryset(self, request):
    qs = super(LocalizedStringAdmin, self).get_queryset(request)
    if request.user.is_superuser:
      return qs

    user_app_ids = AppInfo.objects.user_app_ids_query(request.user)
    keystring_ids = AppInfoKeyString.objects.filter(
      app_info__pk__in=user_app_ids
    ).values_list('key_string__pk', flat=True)
    return qs.filter(Q(key_string__pk__in=keystring_ids))

  def save_model(self, request, obj, form, change):

    if change:
      obj.modified_by = request.user
    else:
      obj.created_by = request.user
    obj.save()


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