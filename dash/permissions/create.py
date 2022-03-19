from dash.models import SkyUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def create_perms(role_name=None, permission_name=None, model=SkyUser):
    content_type = ContentType.objects.get_for_model(model)
    Permission.objects.create(
        codename=permission_name,
        name=role_name,
        content_type=content_type
    )