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

	class Meta(object):
		unique_together = ('name', 'code',)


class AppInfo(models.Model):

	name = models.CharField(max_length=30)
	description =  models.CharField(
		max_length=200, 
		blank=True, 
		null=True)
	base_locale = models.ForeignKey(Locale,
	 	on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % self.name

	def __unicode__(self):
		return '%s' % self.name

	class Meta(object):
		unique_together = ('name',)


class KeyString(models.Model):

	key = models.CharField(max_length=10)
	description =  models.CharField(
		max_length=200,
	 	blank=True, 
	 	null=True)
	
	def __str__(self):
		return "%s" % self.key

	def __unicode__(self):
		return '%s' % self.key

	class Meta(object):
		unique_together = ('key',)


class AppInfoKeyString(models.Model):

	key_string = models.ForeignKey(KeyString,
		on_delete=models.CASCADE)
	app_info = models.ForeignKey(AppInfo, 
		related_name='keys',
		on_delete=models.CASCADE)

	def __str__(self):
		return "%s" % self.key_string__key

	def __unicode__(self):
		return '%s' % self.key_string__key

	class Meta(object):
		unique_together = ('app_info', 'key_string',)


class LocalizableString(models.Model):

	locale = models.ForeignKey(Locale,
	 	on_delete=models.CASCADE)
	value = models.CharField(max_length=1000)
	key_string = models.ForeignKey(KeyString, 
		related_name='values', 
		on_delete=models.CASCADE)

	class Meta(object):
		unique_together = ('locale', 'key_string',)


