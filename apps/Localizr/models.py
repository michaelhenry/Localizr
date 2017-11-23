from django.db import models
from django.conf import settings
from django.utils import timezone

class UserInfoSavableModel(models.Model):

    created     =   models.DateTimeField(auto_now=True)
    modified    =   models.DateTimeField(auto_now_add=True)

    created_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_creators',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_modifiers', 
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Locale(UserInfoSavableModel):

    name        =   models.CharField(max_length=30)
    code        =   models.CharField(max_length=10)
    description =   models.CharField(
        max_length=200, 
        blank=True, 
        null=True)

    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return '%s' % self.name

    class Meta(object):
        unique_together = ('name', 'code',)


class AppInfo(UserInfoSavableModel):

    name        =   models.CharField(max_length=30)
    description =   models.CharField(
        max_length=200, 
        blank=True, 
        null=True)
    slug            =   models.SlugField(max_length=30)
    base_locale     =   models.ForeignKey(Locale, 
        on_delete=models.CASCADE,
        blank=True,
        null=True,)


    def __str__(self):
        return "%s" % self.name

    def __unicode__(self):
        return '%s' % self.name

    class Meta(object):
        unique_together = ('slug',)


class KeyString(UserInfoSavableModel):

    key         =   models.CharField(max_length=100)
    description =   models.CharField(
        max_length=200,
        blank=True, 
        null=True)
    
    def __str__(self):
        return "%s" % self.key

    def __unicode__(self):
        return '%s' % self.key

    class Meta(object):
        unique_together = ('key',)


class AppInfoKeyString(UserInfoSavableModel):

    key_string  =   models.ForeignKey(KeyString, on_delete=models.CASCADE)
    app_info    =   models.ForeignKey(AppInfo, 
        related_name='keys',
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.key_string

    def __unicode__(self):
        return '%s' % self.key_string

    class Meta(object):
        unique_together = ('app_info', 'key_string',)


class LocalizedString(UserInfoSavableModel):

    locale      =   models.ForeignKey(Locale, on_delete=models.CASCADE)
    value       =   models.CharField(max_length=1000)
    key_string  =   models.ForeignKey(KeyString, 
        related_name='values', 
        on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.value

    def __unicode__(self):
        return '%s' % self.value
        
    class Meta(object):
        unique_together = ('locale', 'key_string',)


