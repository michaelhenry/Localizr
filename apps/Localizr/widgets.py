from import_export import widgets


class AppInfoWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):

        app_info = self.model.objects.get_or_create(slug = value)[0]
        if not app_info.name:
            app_info.name = app_info.slug
            app_info.save()
        return app_info


class KeyStringWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):

        keystring = self.model.objects.get_or_create(key = value.strip())[0]
        return keystring


class LocaleWidget(widgets.ForeignKeyWidget):

    def clean(self, value, row=None, *args, **kwargs):

        locale = self.model.objects.get_or_create(code = value)[0]
        if not locale.name:
            locale.name = locale.code
            locale.save()
        return locale
