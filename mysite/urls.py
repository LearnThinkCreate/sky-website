from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(r"", include("django_frontend.urls")),
    path(r'api/', include('dash.urls')),
    path(r"admin/", admin.site.urls),
]
