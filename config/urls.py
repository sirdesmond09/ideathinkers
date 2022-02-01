from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions # new
from drf_yasg.views import get_schema_view # new
from drf_yasg import openapi # new
import debug_toolbar


schema_view = get_schema_view(
    openapi.Info(
        title="Idea Thinkers",
        default_version="v1",
        description="Api documentation for ideathinkersng test",
        terms_of_service="",
        contact=openapi.Contact(email="nnebuedesmond@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/accounts/', include('users.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
