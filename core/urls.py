from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions, routers

# router = routers.SimpleRouter()
# router.register(r'upload', UploadSessionViewSet, basename='upload-session')
#
# schema_view = get_schema_view(
#     openapi.Info(
#         title="API Documentation",
#         default_version="v1",
#         description="Test description",
#         terms_of_service="https://www.google.com/policies/terms/",
#         contact=openapi.Contact(email="test@gmail.com"),
#         license=openapi.License(name="BSD License"),
#     ),
#     public=True,
#     permission_classes=[
#         permissions.AllowAny,
#     ],
# )
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    # path(
    #     'api/swagger<str:format>',
    #     schema_view.without_ui(cache_timeout=0),
    #     name='schema-json',
    # ),
    # path(
    #     "api/swagger/",
    #     schema_view.with_ui("swagger", cache_timeout=0),
    #     name="schema-swagger-ui",
    # ),
    # path(
    #     "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    # ),
    # path('api/v1/', include((router.urls, 'api'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
