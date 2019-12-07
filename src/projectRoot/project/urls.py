
from django.contrib import admin
from django.urls import include, path
from databaseFunctions import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('databaseFunctions/', include('databaseFunctions.urls')),
    path('upload/', views.upload, name='upload')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)