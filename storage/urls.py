from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.homeView,name='homeView'),
    

    # Folder
    path('folders/',views.folders,name='folders'),

    # Files
    path('folder/<str:pk>/',views.singleFolder,name='singleFolder'),
    path('delete-file/<str:pk>/', views.deleteFile, name='deleteFile'),
    path('rename-file/<str:pk>/', views.renameFile, name='renameFile'),
    path('download-file/<str:pk>/', views.downloadFile, name='downloadFile'),
    path('files/', views.files, name='files'),
    path('addFile/', views.addFile, name='addFile'),

    #Folder
    path('rename-folder/<str:pk>/', views.renameFolder, name='renameFolder'),
    path('download-folder/<str:pk>/', views.downloadFolder, name='downloadFolder'),
    path('create-folder/', views.createFolder, name='createFolder'),
    path('delete-folder/<str:pk>/', views.deleteFolder, name='deleteFolder'),

    # API
    path('api/folders/', views.listFolders, name='listFolders'),
    path('api/files/', views.listFiles, name='listFiles'),
    path('api/folders/<str:pk>/', views.listSingleFolder, name='listSingleFolder'),
    path('api/files/<str:pk>/', views.listSingleFile, name='listSingleFile'),
    path('api/folders/<str:pk>/files/', views.listFilesFromFolder, name='listFilesFromFolder'),
    path('api/driveinfo/', views.driveInfo, name='driveInfo'),
    path('api/files/<str:pk>/delete/', views.deleteFileAPI, name='deleteFileAPI'),
    path('api/files/<str:pk>/edit/', views.editFileAPI, name='editFileAPI'),
    path('api/files/<str:pk>/download/', views.downloadFileAPI, name='downloadFileAPI'),

    # API Keys
    path('api-keys/',views.listApiKeys,name='listApiKeys'),
    path('api-keys/create/',views.createApiKeys,name='createApiKeys'),
    path('api-keys/delete/<str:pk>/',views.deleteApiKeys,name='deleteApiKeys')
]