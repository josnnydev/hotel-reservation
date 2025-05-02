 
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
 
 
schema_view = get_schema_view(
    openapi.Info(
        title="Hotel API",
        default_version='v1',
        description="API para reservas de hotel",
    ),
    public=True,
    permission_classes=[], 
)
 

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api-token-auth/', obtain_auth_token),
    path('api/', include('reservation.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
     
   
]
