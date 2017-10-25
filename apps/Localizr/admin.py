from django.contrib import admin

from .models import (
	Locale,
	AppInfo,
	KeyString,
	LocalizableString,
	)


class LocalizableStringInline(admin.TabularInline):

	model = LocalizableString
	extra = 1


class LocaleAdmin(admin.ModelAdmin):

	ordering = ('name','code',)
	search_fields = ('name','code',)
	list_display = ('name' ,'code','description')
	
	
class AppInfoAdmin(admin.ModelAdmin):

	ordering = ('name',)
	search_fields = ('name','description',)
	list_display = ('name' ,'description','base_locale')
	

class KeyStringAdmin(admin.ModelAdmin):
	ordering = ('key',)
	search_fields = ('key',)
	list_display = ('key' ,'description',)
	list_filter = ('app_info',)
	inlines = [LocalizableStringInline,]


admin.site.register(Locale, LocaleAdmin)
admin.site.register(AppInfo)
admin.site.register(KeyString, KeyStringAdmin)
admin.site.site_header = 'Localizr'