from django.contrib import admin

from .models import (
	Locale,
	AppInfo,
	KeyString,
	AppInfoKeyString,
	LocalizableString,
	)


class LocaleAdmin(admin.ModelAdmin):

	ordering 		= 	('name','code',)
	search_fields 	= 	('name','code',)
	list_display 	= 	('name' ,'code','description')
	

class AppInfoAdmin(admin.ModelAdmin):

	ordering 		= 	('name',)
	search_fields 	= 	('name','description',)
	list_display 	= 	('name' ,'description','base_locale')
	

class LocalizableStringInline(admin.TabularInline):

	model = LocalizableString
	extra = 1


class KeyStringAdmin(admin.ModelAdmin):

	ordering 		=	 ('key',)
	search_fields 	= 	 ('key','description',)
	list_display 	=	 ('key' ,'description',)
	inlines 		=	 [LocalizableStringInline,]

	
class AppInfoKeyStringAdmin(admin.ModelAdmin):
	ordering 			=	 ('key_string', 'app_info',)
	search_fields 		=	 ('key_string__key',)
	list_display 		=	 ('app_info' ,'key_string',)
	list_filter 		=	 ('app_info',)
	autocomplete_fields = 	 ['key_string', 'app_info']


admin.site.register(Locale, LocaleAdmin)
admin.site.register(AppInfo, AppInfoAdmin)
admin.site.register(KeyString, KeyStringAdmin)
admin.site.register(AppInfoKeyString, AppInfoKeyStringAdmin)
admin.site.site_header = 'Localizr'