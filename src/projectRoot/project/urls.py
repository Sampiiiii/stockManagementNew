
from django.contrib import admin
from django.urls import include, path
from databaseFunctions import views_database_functions
from core import views_core
from graphingModule import views_graphing_module
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views_core.Home.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('documents/', views_database_functions.document_list, name='document_list'),
    path('documents/upload', views_database_functions.upload_document, name='upload_document'),
    path('documents/<int:pk>/', views_database_functions.delete_document, name='delete_document'),
    path('documents/process/<int:pk>/', views_database_functions.process_document, name='process_document'),
    path('products/', views_database_functions.product_list, name='product_list'),
    path('products/delete/<int:pk>', views_database_functions.delete_product, name='delete_product'),
    path('products/delete/all', views_database_functions.delete_all_products, name='delete_all_products'),
    path('products/modify/<int:pk>/',views_database_functions.modify_product, name='modify_product'),
    path('products/add', views_database_functions.product_add, name='product_add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)