from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register',views.register, name='register'),
    path('', views.home, name='home'),
    path('about',views.about, name='about'),
    path('myfiles/<str:pk>',views.folders, name='myfiles'),    
    path('upload/<int:pk>',views.uploading, name='upload'),
    path('folder/<int:folder_id>', views.folder_contents, name='folder_contents'),
    path('download/<str:file_name>',views.download_file, name='download'),
    # path('download-folder-zip/',views.download_folder_zip,name='download_folder_zip'),
    path('delete/<int:pk>',views.delete_file, name='delete'),
    path('delete-folder/<int:pk>' ,views.delete_folder, name='delete_folder'),
    path('login',views.login,name='login'),
    path('logout', views.logout, name='logout'),
    
]