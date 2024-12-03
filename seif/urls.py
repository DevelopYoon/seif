from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularJSONAPIView, SpectacularYAMLAPIView, SpectacularSwaggerView, SpectacularRedocView

#웹페이지
from django.conf.urls.static import static
from django.conf import settings
from www.views import upload_image
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #웹페이지
    path('admin/', admin.site.urls),
    path('', include('www.urls')),  # Ensure this points to your app's URLs
    path('img/', upload_image, name='upload_image'),




    # DRF Spectacular schema and documentation endpoints
    path('api/schema/json/', SpectacularJSONAPIView.as_view(), name='schema-json'),
    path('api/schema/yaml/', SpectacularYAMLAPIView.as_view(), name='schema-yaml'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema-json'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema-json'), name='redoc'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
