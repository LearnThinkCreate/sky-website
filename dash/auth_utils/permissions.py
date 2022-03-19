from dash.models import SkyUser
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .permissions_dict import PERMISSIONS
from django.shortcuts import get_object_or_404

def update_user_perms(user_id, roles):
    user = get_object_or_404(SkyUser, pk=user_id)

    for p in PERMISSIONS:
        has_role = p['role_name'] in roles
        has_perm = user.has_perm('dash.' + p['permission_name'])
        if has_perm and has_role:
            continue
        
        # Permission needs to be granted or removed 
        content_type = ContentType.objects.get_for_model(SkyUser)
        permission = Permission.objects.get(
            codename=p['permission_name'],
            content_type=content_type
        )

        if has_role and not has_perm:
            # Grant permission
            user.user_permissions.add(permission)
        if has_perm and not has_role:
            # Remove permission
            user.user_permissions.remove(permission)

def create_perms(role_name=None, permission_name=None, model=SkyUser):
    content_type = ContentType.objects.get_for_model(model)
    Permission.objects.create(
        codename=permission_name,
        name=role_name,
        content_type=content_type
    )