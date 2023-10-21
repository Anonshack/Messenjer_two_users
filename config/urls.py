from django.contrib import admin
from django.urls import path, include

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from django.views.generic import TemplateView

schema_view = get_schema_view(
   openapi.Info(
      title="Social network API",
      default_version='v1',
      description="API for Social networking app",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="princeasia013@gmail.com"),
      license=openapi.License(name="No licence"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/accounts/', include('users.urls')),
    path('api/v1/chats/', include('app_chat.urls')),
    path('api/v1/pages/', include('pages.urls')),
    # path('api/v1/', include('.urls')),
#   For API documentation
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
