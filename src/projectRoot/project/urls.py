
from django.contrib import admin
from django.urls import include, path
from databaseFunctions import views
from core import views2
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views2.Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload', views.upload_document, name='upload_document'),
    path('documents/<int:pk>/', views.delete_document, name='delete_document'),
    path('documents/process/<int:pk>/', views.process_document, name='process_document'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)