from django.contrib import admin
from django.urls import path , include
from project import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/core/',include('core.urls')),
    path('api/users/',include('accounts.urls')),
    path('api/reports/',include('reports.urls')),
    path('api/departments/',include('departments.urls')),

    path('api/',include('djoser.urls')),
    path('admin/', admin.site.urls),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)