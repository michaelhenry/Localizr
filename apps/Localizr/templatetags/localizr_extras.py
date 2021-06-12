import sys
from django import template
from django.conf import settings

register = template.Library()


@register.filter
def sorted_apps(value):

    if not hasattr(settings, 'ADMIN_DASHBOARD_LAYOUT'):
        return value

    app_layout = settings.ADMIN_DASHBOARD_LAYOUT

    def _get_app_sequence(app):
        return app_layout.get(app['app_label'], {}).get('sequence', sys.maxsize)

    def _get_model_sequence(app, model):
        models = app_layout.get(app['app_label'], {}).get('models', [])
        return models.index(model["object_name"]) if model["object_name"] in models else sys.maxsize

    def _update_app(app):

        models = app['models']
        models.sort(
            key=lambda x: _get_model_sequence(app, x)
        )
        app['models'] = models
        return app

    app_list = value
    app_list.sort(
        key=lambda x: _get_app_sequence(x)
    )
    app_list = list(map(lambda x: _update_app(x), app_list))
    return app_list
