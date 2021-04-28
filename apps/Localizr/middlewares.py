from django.utils.deprecation import MiddlewareMixin
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, HttpResponseGone
from datetime import timedelta
from django.utils import timezone
from .models import (
    Snapshot,
    SnapshotFile,
)


class LocalizrSnapshotMiddleWare(MiddlewareMixin):

    def process_response(self, request, response):

        snapshot_key = request.GET.get('snapshot')
        format = request.GET.get('format')
        if snapshot_key and format:

            filename = request.path.split('/')[-1]
            locale_code = filename.split('.')[-1]
            app_slug = filename.split('.')[0]
            content_type = response['Content-Type']

            snapshot, created = Snapshot.objects.get_or_create(
                key=snapshot_key,
                app_slug=app_slug,
                format=format,
            )

            if not created:
                snapshot_file = None
                snapshot_file_query = SnapshotFile.objects.filter(
                    snapshot=snapshot,
                    locale_code=locale_code)

                if snapshot_file_query.exists():
                    snapshot_file = snapshot_file_query.first()
                else:

                    if timezone.now() > (snapshot.created + timedelta(hours=12)):
                        return HttpResponseGone()
                    content = response.content

                    snapshot_file = SnapshotFile(
                        snapshot=snapshot, locale_code=locale_code)
                    snapshot_file.key = snapshot_key
                    snapshot_file.file.save(filename, ContentFile(content))
                    snapshot_file.save()

                return HttpResponseRedirect(snapshot_file.file.url, content_type=content_type)
        return response


class CorsMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        pass

    def process_response(self, request, response):

        # For now it's a wildcard.
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Host, X-Date'
        return response
