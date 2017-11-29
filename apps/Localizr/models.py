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
        unique_together     =   ('name', 'code',)
        verbose_name        =   'Locale'
        verbose_name_plural =   'Locales'


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
        unique_together     =   ('slug',)
        verbose_name        =   'App'
        verbose_name_plural =   'Apps'


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
        unique_together     =    ('key',)
        verbose_name        =    'Key'
        verbose_name_plural =    'Keys'
        

class AppInfoKeyStringQuerySet(models.QuerySet):


    def key_value_filter(self, app, locale_code):

        all_key_strings = self.filter(
            app_info__slug=app.slug,
        )

        localized_strings_query = all_key_strings.filter(
            key_string__values__locale__code=locale_code
        ).values(
            'key_string__key',
            'key_string__values__value'
        ).order_by('key_string__key')

        if app.base_locale:
            
            # just create a new queryset to avoid evaluation of the localized_string_query
            localized_ids_query = all_key_strings.filter(
                key_string__values__locale__code=locale_code
            ).values_list(
                'key_string__pk',
                flat=True
            )

            # then check for missing ones by excluding the found ones
            missing_strings_query = all_key_strings.filter(
                key_string__values__locale__code=app.base_locale.code
            ).exclude(key_string__pk__in=localized_ids_query).values(
                'key_string__key',
                'key_string__values__value'
            )

            localized_strings_query = localized_strings_query | missing_strings_query
        return localized_strings_query


class AppInfoKeyStringManager(models.Manager):

    def get_queryset(self):
        return AppInfoKeyStringQuerySet(self.model)


class AppInfoKeyString(UserInfoSavableModel):

    key_string  =   models.ForeignKey(KeyString, on_delete=models.CASCADE)
    app_info    =   models.ForeignKey(AppInfo, 
        related_name='keys',
        on_delete=models.CASCADE)
    
    objects = AppInfoKeyStringManager()

    def __str__(self):
        return "%s" % self.key_string

    def __unicode__(self):
        return '%s' % self.key_string

    class Meta(object):
        unique_together     =    ('app_info', 'key_string',)
        verbose_name        =    'App \'s Key'
        verbose_name_plural =    'App \'s Keys'


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
        unique_together     =    ('locale', 'key_string',)
        verbose_name        =    'Localized String'
        verbose_name_plural =    'Localized Strings'


