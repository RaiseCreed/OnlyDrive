from .models import Folder, File
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def getFiles(request):
    
    searchFor = request.GET.get("q") if request.GET.get("q") != None else ""

    files = File.objects.filter(
        Q(user__exact=request.user) &
        ( 
        Q(name__icontains=searchFor) |
        Q(folder__name__icontains=searchFor) |
        Q(extension__icontains=searchFor)
        )
    )

    return files, searchFor


def getFolder(request):
    
    searchFor = request.GET.get("q") if request.GET.get("q") != None else ""

    folder = Folder.objects.filter(
        Q(user__exact=request.user) &
        ( 
        Q(name__icontains=searchFor)
        )
    )

    return folder, searchFor


def paginateObjects(request, objects, results):

    page = request.GET.get('page') if request.GET.get('page') != None else 1

    paginator = Paginator(objects, results)

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        objects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        objects = paginator.page(page)

    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1

    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex,rightIndex)
    

    return objects, custom_range