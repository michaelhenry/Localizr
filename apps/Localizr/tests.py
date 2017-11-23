import json

from django.contrib.auth.models import User, Permission
from django.test import (
    TestCase,
    Client,
    )

from .models import (
    Locale,
    AppInfo,
    KeyString,
    AppInfoKeyString,
    LocalizedString,
    )


def jsonify(content="{}"):
    return json.loads(content.decode('utf-8'))

class LocalizrTest(TestCase):

    def setUp(self):

        self.client = Client()

        username = "kel"
        password = "12345dad216790oeieiuri3urieure"
        email = "me@iamkel.net"

        localizr_permissions = Permission.objects.filter(
            codename__contains='_localizr'
        )

        self.user = User.objects.create_user(
            username=username, email=email, password=password)
        self.user.user_permissions.set(list(localizr_permissions))
        self.client.login(username=username, password=password)
      

    def test_create_locale(self):

        locale_en = Locale(name='English', code='en',)
        locale_en.save()
        self.assertEqual(locale_en.code, 'en')


    def test_create_app(self):

        app = AppInfo(name='DemoApp', slug='demo-app',)
        app.save()
        self.assertEqual(app.slug, 'demo-app')


    def test_create_keystring(self):

        key_string = KeyString(key='NEXT',)
        key_string.save()

        self.assertEqual(key_string.key, 'NEXT')


    def test_create_localized_strings_of_keystring(self):

        key_string = KeyString(key='NEXT',)
        key_string.save()

        locale = Locale(name='English', code='en',)
        locale.save()
        value = 'Next'
        locstring = LocalizedString(key_string=key_string,locale=locale,value=value)
        locstring.save()

        locale = Locale(name='Japanese', code='ja',)
        locale.save()
        value = '次'
        locstring = LocalizedString(key_string=key_string,locale=locale,value=value)
        locstring.save()

        locale = Locale(name='Chinese', code='zh',)
        locale.save()
        value = '下一个'
        locstring = LocalizedString(key_string=key_string,locale=locale,value=value)
        locstring.save()

        values = list(map(lambda x: x.value, list(key_string.values.all())))
        self.assertEqual(key_string.key, 'NEXT')
        self.assertEqual(len(values), 3)
        self.assertEqual('Next' in values, True)
        self.assertEqual('次' in values, True)
        self.assertEqual('下一个' in values, True)
        