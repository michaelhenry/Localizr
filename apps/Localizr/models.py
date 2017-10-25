from django.db import models

class Locale(models.Model):

	name = models.CharField(max_length=30)
	code = models.CharField(max_length=10)
	description =  models.CharField(
		max_length=200, 
		blank=True, 
		null=True)

	def __str__(self):
		return "%s" % self.name

	def __unicode__(self):
		return '%s' % self.name


class AppInfo(models.Model):

	name = models.CharField(max_length=30)
	description =  models.CharField(
		max_length=200, 
		blank=True, 
		null=True)
	base_locale = models.ForeignKey(Locale)

	def __str__(self):
		return "%s" % self.name

	def __unicode__(self):
		return '%s' % self.name


class KeyString(models.Model):

	key = models.CharField(max_length=10)
	description =  models.CharField(
		max_length=200,
	 	blank=True, 
	 	null=True)
	app_info = models.ForeignKey(AppInfo, 
		related_name='keys')

	def __str__(self):
		return "%s" % self.key

	def __unicode__(self):
		return '%s' % self.key


class LocalizableString(models.Model):

	locale = models.ForeignKey(Locale)
	value = models.CharField(max_length=1000)
	key_string = models.ForeignKey(KeyString, 
		related_name='values')


