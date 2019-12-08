
from django.contrib import admin
from django.urls import include, path
from databaseFunctions import views
from core import views2
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views2.Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('databaseFunctions/', include('databaseFunctions.urls')),
    path('documents/', views.document_list, name='document_list'),
    path('documents/upload', views.upload_document, name='upload_document'),
    path('documents/<int:pk>/', views.delete_document, name='delete_document'),

    path('class/documents/', views.DocumentList.as_view(), name='DocumentList'),
    path('class/documents/upload', views.DocumentUpload.as_view(), name='UploadDocument'),

    path('upload/', views.upload, name='upload')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)