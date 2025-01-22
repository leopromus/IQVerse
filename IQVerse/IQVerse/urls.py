from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static


# Define the schema view for Swagger UI
schema_view = get_schema_view(
   openapi.Info(
      title="IQVerse API",
      default_version='v1',
      description="API documentation for the IQVerse quiz application",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@iqverse.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/', include('quiz.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-ui'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)