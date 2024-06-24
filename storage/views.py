from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated
from .models import Folder, File
import os
import zipfile
from django.core.signals import request_finished
from django.http import FileResponse
from django.utils import timezone
from .serializers import FolderSerializer, FileSerializer
from django.conf import settings
from typing import List
import threading
import time
import math
from django.db.models import Q
from .utils import getFiles, getFolder, paginateObjects
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
import pickle as pk


def getDirSize(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def getDriveSpaceInfo():
    totalSpace = 5.00 # GB
    usedSpace = round((getDirSize(os.path.join(settings.MEDIA_ROOT, os.path.join(f"files/"))))/1024/1024/1024,2)
    freeSpace = round(totalSpace - usedSpace,2)
    percent = (usedSpace/totalSpace) * 100
    
    return {'total':totalSpace,'used':usedSpace,'free':freeSpace,'percent':percent}

# Create your views here.
def remove_file(path):
    time.sleep(5) 
    if os.path.exists(path):
        os.remove(path)

@login_required(login_url='login')
def homeView(request):

    folders = Folder.objects.filter(
        Q(user__exact=request.user)
    ).order_by('-files_count')[:4]

    files = File.objects.filter(
        Q(user__exact=request.user)
    ).order_by('-modified')[:5]
    

    context = {'folders':folders,'files':files}
    context.update(getDriveSpaceInfo()) 
    return render(request, 'home.html',context=context)

@login_required(login_url='login')
def folders(request):
    folders, searchFor = getFolder(request)
    folders, custom_range = paginateObjects(request,folders,9)

    context = {'folders':folders,'searchFor':searchFor,'custom_range':custom_range}
    context.update(getDriveSpaceInfo())
    return render(request, 'folders.html', context=context)

@login_required(login_url='login')
def singleFolder(request,pk):
    
    searchFor = request.GET.get("q") if request.GET.get("q") != None else ""

    try:
        folder = Folder.objects.get(id=pk)
    except Folder.DoesNotExist:
        return render(request, '404.html')
    

    if request.method == 'POST':
        fileData = request.FILES.get('fileBody')

        if fileData:
            filename, file_extension = os.path.splitext(fileData.name)

            uploadedFile = File(
                content=fileData,
                name=filename,
                extension=file_extension,
                size=fileData.size,
                folder=Folder.objects.get(id=pk),
                user=request.user
            )
            uploadedFile.save()

    files = folder.file_set.filter(
        Q(user__exact=request.user) &
        ( 
        Q(name__icontains=searchFor) |
        Q(extension__icontains=searchFor)
        )
    )

    files, custom_range = paginateObjects(request,files,20)

    context = {'folder':folder,'files':files,'custom_range':custom_range,'searchFor':searchFor}
    context.update(getDriveSpaceInfo())
    return render(request, 'single-folder.html', context=context)

@login_required(login_url='login')
def files(request):

    files, searchFor = getFiles(request)
    files, custom_range = paginateObjects(request,files,20)

    context = {'files':files,'searchFor':searchFor,'custom_range':custom_range}
    context.update(getDriveSpaceInfo())
    return render(request, 'files.html',context=context)
                  
@login_required(login_url='login')
def deleteFile(request, pk):

    try:
        file = File.objects.get(id=pk)
    except File.DoesNotExist:
        return render(request, '404.html')
    
    if request.method == 'POST':
        folder = file.folder
        file.delete()
        folder.decrease_file_counter
        return redirect('singleFolder',folder.id)
    
    context = {'object':file}
    context.update(getDriveSpaceInfo())
    return render(request, 'delete-object.html',context=context)

@login_required(login_url='login')
def renameFile(request, pk):

    try:
        file = File.objects.get(id=pk)
    except File.DoesNotExist:
        return render(request, '404.html')
    
    if request.method == 'POST':
        newFilename = request.POST.get('newFilename')

        if newFilename:
            filename, file_extension = os.path.splitext(newFilename)
            file.name = filename
            file.extension = file_extension
            file.modified = timezone.now()
            file.save()
            
        return redirect('singleFolder', file.folder.id)

    context = {'object':file}
    context.update(getDriveSpaceInfo())
    return render(request, 'rename-file.html',context=context)

@login_required(login_url='login')
def downloadFile(request, pk):

    try:
        file = File.objects.get(id=pk)
    except File.DoesNotExist:
        return render(request, '404.html')
    
    return FileResponse(open(os.path.join(settings.MEDIA_ROOT, os.path.join(f"files/",str(file.user.id), str(file.id))), 'rb'),as_attachment=True,filename=file.get_full_name)

@login_required(login_url='login')
def addFile(request):
    context = {}

    if request.method == 'POST':
        fileData = request.FILES.get('file')
        folderId = request.POST.get('folder')

        if fileData and folderId:
            filename, file_extension = os.path.splitext(fileData.name)

            uploadedFile = File(
                content=fileData,
                name=filename,
                extension=file_extension,
                size=fileData.size,
                folder=Folder.objects.get(id=folderId),
                user=request.user
            )
            uploadedFile.save()
            return redirect('files')
        else:
            context.update({'message':'Please select file and one of the folders!'})

    context.update({'folders':Folder.objects.filter(user__exact=request.user)})
    context.update(getDriveSpaceInfo())
    return render(request, 'add-file.html',context=context)

@login_required(login_url='login')
def renameFolder(request, pk):

    try:
        folder = Folder.objects.get(id=pk)
    except Folder.DoesNotExist:
        return render(request, '404.html')

    if request.method == 'POST':
        newFolderName = request.POST.get('newFolderName')

        if newFolderName:
            folder.name = newFolderName
            folder.save()

        return redirect('folders')

    context = {'object':folder}
    context.update(getDriveSpaceInfo())
    return render(request, 'rename-folder.html', context=context)

@login_required(login_url='login')
def downloadFolder(request, pk):

    try:
        folder = Folder.objects.get(id=pk)
    except Folder.DoesNotExist:
        return render(request, '404.html')


    files: List[File] = folder.file_set.all()
    temp_zip_path = os.path.join(settings.MEDIA_ROOT,'files/archive.zip')

    with zipfile.ZipFile(temp_zip_path, 'w') as zip_file:
        for plik in files:
            file_path = os.path.join(settings.MEDIA_ROOT, os.path.join(f"files/",str(plik.user.id), str(plik.id)))
            
            zip_file.write(file_path, arcname=plik.get_full_name)
    
    response = FileResponse(open(temp_zip_path, 'rb'),as_attachment=True,filename=f"{folder.name}.zip")


    # Starting another, delayed thread for deleting temponary archive.
    thread = threading.Thread(target=remove_file, args=(temp_zip_path,))
    thread.start()

    return response

@login_required(login_url='login')
def createFolder(request):
    folderName = request.POST.get('folderName')

    if folderName:
        newFolder = Folder(
            name=folderName,
            user=request.user
        )
        newFolder.save()

        return redirect('folders')

    context = {}
    context.update(getDriveSpaceInfo())
    return render(request, 'create-folder.html', context=context)

@login_required(login_url='login')
def deleteFolder(request, pk):
    try:
        folder = Folder.objects.get(id=pk)
    except Folder.DoesNotExist:
        return render(request, '404.html')

    if request.method == 'POST':
        folder.delete()
        return redirect('folders')
    
    context = {'object':folder}
    context.update(getDriveSpaceInfo())

    return render(request, 'delete-object.html',context=context)

@login_required(login_url='login')
def listApiKeys(request):
    
    keys = APIKey.objects.all()

    context = {'keys':keys}
    context.update(getDriveSpaceInfo())
    return render(request, 'keys.html',context=context)

@login_required(login_url='login')
def createApiKeys(request):
    context = {}

    if request.method == 'POST':
        keyName = request.POST.get('keyName')
        keyDate = request.POST.get('keyDate')
        allowedMethods = []

        if request.POST.get('methodGet'):
            allowedMethods.append('GET')
        if request.POST.get('methodPost'):
            allowedMethods.append('POST')
        if request.POST.get('methodPatch'):
            allowedMethods.append('PATCH')
        if request.POST.get('methodDelete'):
            allowedMethods.append('DELETE')

        if keyName and keyDate and allowedMethods:
            api_key, key = APIKey.objects.create_key(name=keyName,allowed_methods=','.join(allowedMethods),expiry_date=keyDate)

            context.update({'message':'Your API Key: '+key})
        else:
            context.update({'message':'Please fill key name, expiration date and at least one allowed method!'})
    
    context.update(getDriveSpaceInfo())
    return render(request, 'create-key.html',context=context)

@login_required(login_url='login')
def deleteApiKeys(request, pk):
    
    try:
        key = APIKey.objects.get(id=pk)
    except APIKey.DoesNotExist:
        return render(request, '404.html')

    if request.method == 'POST':
        key.delete()

        return redirect('listApiKeys')

    context = {'object':key}
    context.update(getDriveSpaceInfo())
    return render(request, 'delete-object.html',context=context)


# API

@api_view(['GET'])
def listFolders(request):
    folders = Folder.objects.all()
    serializer = FolderSerializer(folders, many=True)
    response = {
        'data':serializer.data
    }
    return Response(response)


@api_view(['GET'])
def listFiles(request):
    files = File.objects.all()
    serializer = FileSerializer(files, many=True)
    response = {
        'data':serializer.data
    }
    return Response(response)


@api_view(['GET'])
def listSingleFile(request,pk):
    try:
        file = File.objects.get(id=pk)
    except File.DoesNotExist:
        return Response({"Error":"File not found"},status=status.HTTP_404_NOT_FOUND)

    if file:
        serializer = FileSerializer(file, many=False)
        response = {
            'data':serializer.data
        }
        return Response(response)


@api_view(['GET'])
def listSingleFolder(request,pk):
    try:
        folder = Folder.objects.get(id=pk)
    except Folder.DoesNotExist:
        return Response({"Error":"Folder not found"},status=status.HTTP_404_NOT_FOUND)

    if folder:
        serializer = FolderSerializer(folder, many=False)
        response = {
            'data':serializer.data
        }
        return Response(response)
    


@api_view(['GET'])
def listFilesFromFolder(request,pk):
    try:
        folder = Folder.objects.get(id=pk)
    except Folder.DoesNotExist:
        return Response({"Error":"Folder not found"},status=status.HTTP_404_NOT_FOUND)

    if folder:
        files = folder.file_set.all()
        serializer = FileSerializer(files, many=True)
        response = {
            'data':serializer.data
        }
        return Response(response)
    

@api_view(['GET'])
def driveInfo(request):
    data = getDriveSpaceInfo()
    data.update({'unit':'GB'})
    return Response(data)


@api_view(['DELETE'])
def deleteFileAPI(request,pk):

    try:
        file = File.objects.get(id=pk)
    except File.DoesNotExist:
        return Response({"Error":"File not found"}, status=status.HTTP_404_NOT_FOUND)
    
    file.delete()

    return Response({"Success":"File deleted"},status=status.HTTP_202_ACCEPTED)



@api_view(['PATCH'])
def editFileAPI(request,pk):

    try:
        file = File.objects.get(id=pk)
    except File.DoesNotExist:
        return Response({"Error":"File not found"}, status=status.HTTP_404_NOT_FOUND)
    
    updated = False

    if "name" in request.data:
        filename, file_extension = os.path.splitext(request.data["name"])
        file.name = filename
        file.extension = file_extension
        updated = True

    if "folder" in request.data:

        try:
            folder = Folder.objects.get(id=request.data["folder"])
        except Folder.DoesNotExist:
            return Response({"Error":"Folder not found"}, status=status.HTTP_404_NOT_FOUND)

        file.folder = folder
        updated = True

    if updated:
        file.modified = timezone.now()
        file.save()

    return Response({"Success":"File modified"},status=status.HTTP_202_ACCEPTED)
    

    
@api_view(['GET'])
def downloadFileAPI(request,pk):
    try:
        file = File.objects.get(id=pk)
    except File.DoesNotExist:
        return Response({"Error":"File not found"}, status=status.HTTP_404_NOT_FOUND)

    return FileResponse(open(os.path.join(settings.MEDIA_ROOT, os.path.join(f"files/", str(file.user.id), str(file.id))), 'rb'), as_attachment=True, filename=file.get_full_name)


