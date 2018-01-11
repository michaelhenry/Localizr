from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import Q, F, OuterRef, Subquery
from django.contrib.auth.models import Group
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


    def filter_by_locale_code(self, locale_code):

        base_value = LocalizedString.objects.filter(
            locale=OuterRef('app_info__base_locale')
        ).filter(
            key_string=OuterRef('key_string'),
        ).values_list('value',flat=True)

        value = LocalizedString.objects.filter(
            locale__code=locale_code
        ).filter(
            key_string=OuterRef('key_string'),
        ).values_list('value',flat=True)

        return self\
            .annotate(
                key=F('key_string__key'), 
                value=Coalesce(
                    Subquery(value), 
                    Subquery(base_value)))\
            .values_list('key','value')


class AppInfoKeyStringManager(models.Manager):

    def get_queryset(self):
        return AppInfoKeyStringQuerySet(self.model)


class AppInfoKeyString(UserInfoSavableModel):

    key_string  =   models.ForeignKey(KeyString, on_delete=models.CASCADE)
    app_info    =   models.ForeignKey(AppInfo, 
        related_name='keys',
        on_delete=models.CASCADE)
    
    objects = AppInfoKeyStringManager()

    # just placeholder
    def value(self):
        return ""

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


class Snapshot(UserInfoSavableModel):

    key      = models.CharField(max_length=36,)
    app_slug = models.CharField(max_length=30)
    format   = models.CharField(max_length=10)
    
    def __str__(self):
        return "%s" % (self.key)

    def __unicode__(self):
        return '%s' % (self.key)

    class Meta(object):
        unique_together     =    ('key', 'app_slug','format',)
        verbose_name        =    'Snapshot'
        verbose_name_plural =    'Snapshots'

def snapshot_folder(instance,filename):

    return "%s/%s/snapshots/%s/%s" % (
        instance.snapshot.app_slug,
        instance.snapshot.format, 
        instance.snapshot.key, 
        filename
        )

class SnapshotFile(UserInfoSavableModel):

    snapshot    = models.ForeignKey(Snapshot, 
        related_name='snapshots', 
        on_delete=models.CASCADE)
    locale_code = models.CharField(max_length=10)
    file        = models.FileField(upload_to=snapshot_folder)

    def __str__(self):
        return "%s" % (
            self.file.name
            )

    def __unicode__(self):
        return "%s" % (
            self.file.name, 
            )

    class Meta(object):
        unique_together     =    ('snapshot', 'locale_code',)
        verbose_name        =    'SnapshotFile'
        verbose_name_plural =    'SnapshotFiles'


class AppUser(UserInfoSavableModel):

    app_info = models.ForeignKey(AppInfo, 
        on_delete=models.CASCADE)
    user     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,)

    def __str__(self):
        return "%s|%s" % (
            self.user.username, self.app_info.slug
            )

    def __unicode__(self):
        return "%s|%s" % (
            self.user.username, self.app_info.slug
            )

    class Meta(object):
        unique_together     =    ('app_info', 'user',)
        verbose_name        =    'User-App Permission'
        verbose_name_plural =    'User-App Permissions'

class AppUserGroup(UserInfoSavableModel):

    app_info = models.ForeignKey(AppInfo, 
        on_delete=models.CASCADE)
    group     = models.ForeignKey(Group,
        on_delete=models.CASCADE,)

    def __str__(self):
        return "%s|%s" % (
            self.group.name, self.app_info.slug
            )

    def __unicode__(self):
        return "%s|%s" % (
            self.group.name, self.app_info.slug
            )

    class Meta(object):
        unique_together     =    ('app_info', 'group',)
        verbose_name        =    'User-Group-App Permission'
        verbose_name_plural =    'User-Group-App Permissions'


# Extension method for AppInfo.objects
def user_app_ids_query(user):

    q = None
    if user.is_superuser:
        q = AppInfo.objects.all()
    else:
        user_app_ids = AppUser.objects.filter(
            user=user
        ).values_list('app_info__pk', flat=True)

        group_app_ids = AppUserGroup.objects.filter(
            group_id__in=user.groups.values_list('id', flat=True)
        ).values_list('app_info__pk', flat=True)

        q = AppInfo.objects.filter(Q(pk__in=group_app_ids) | Q(pk__in=user_app_ids))
    return q.values_list('id')

setattr(AppInfo.objects, "user_app_ids_query", user_app_ids_query)

