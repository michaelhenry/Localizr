python manage.py migrate

cat <<EOF | python manage.py shell
import os
from django.contrib.auth.models import User
if os.environ.get("ADMIN_USERNAME", None):
	User.objects.filter(username="$ADMIN_USERNAME").exists() or \
		User.objects.create_superuser("$ADMIN_USERNAME", "$ADMIN_EMAIL", "$ADMIN_PASSWORD")
EOF

python manage.py collectstatic --noinput
gunicorn LocalizrExample.wsgi
