from rest_framework import serializers

from .models import (
	Locale,
	AppInfo,
	KeyString,
	AppInfoKeyString,
	LocalizedString,
	)

class LocaleSerializer(serializers.ModelSerializer):
	
	"""
	LocaleSerializer
	"""

	class Meta:
		model = Locale
		fields = (
			'id', 
			'name', 
			'code', 
			'description'
			)


class AppInfoSerializer(serializers.ModelSerializer):
	
	"""
	AppInfoSerializer
	"""

	class Meta:
		model = AppInfo
		fields = (
			'id', 
			'name', 
			'slug',
			'base_locale', 
			'description'
			)


class KeyStringSerializer(serializers.ModelSerializer):
	
	"""
	KeyString
	"""

	class Meta:
		model = KeyString
		fields = (
			'id', 
			'key', 
			'description',
			)


class AppInfoKeyStringSerializer(serializers.ModelSerializer):
	
	"""
	AppInfoKeyString
	"""

	class Meta:
		model = AppInfoKeyString
		fields = (
			'id', 
			'app_info', 
			'key_string',
			)


class KeyValueSerializer(serializers.Serializer):
	
	key = serializers.SerializerMethodField()
	value = serializers.SerializerMethodField()

	def get_key(self, obj):
		return obj[0]
	
	def get_value(self, obj):
		return obj[1]
