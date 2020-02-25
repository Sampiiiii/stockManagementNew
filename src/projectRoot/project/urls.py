
from django.contrib import admin
from django.urls import include, path
from databaseFunctions import views_database_functions as vdf
from core import views_core as vc
from graphingModule import views_graphing_module as vgm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', vc.Home.as_view(), name='home'),
    path('admin/', admin.site.urls),

    path('documents/', vdf.document_list, name='document_list'),
    path('documents/upload', vdf.upload_document, name='upload_document'),
    path('documents/<int:pk>/', vdf.delete_document, name='delete_document'),
    path('documents/process/<int:pk>/', vdf.process_document, name='process_document'),

    path('products/', vdf.product_list, name='product_list'),
    path('products/view/<int:pk>', vgm.view_product, name='view_product'),
    path('products/delete/<int:pk>', vdf.delete_product, name='delete_product'),
    path('products/delete/all', vdf.delete_all_products, name='delete_all_products'),
    path('products/modify/<int:pk>/',vdf.modify_product, name='modify_product'),
    path('products/add', vdf.product_add, name='product_add'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)