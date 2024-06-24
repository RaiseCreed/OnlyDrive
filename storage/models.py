from django.db import models
from uuid import uuid4
from users.models import User
import os
from django.conf import settings

# Create your models here.

def generate_uuid():
    return str(uuid4())

class Folder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    files_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
    @property
    def decrease_file_counter(self):
        self.files_count -= 1
        self.save()

    class Meta:
        ordering = ['name']

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=generate_uuid, editable=False)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def generate_filename(self, filename):
        return os.path.join(f"files/{self.user.id}/", self.id)
    
    content = models.FileField(blank=False, null=False,upload_to=generate_filename)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    extension = models.CharField(max_length=10)
    size = models.IntegerField()
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)


    def __str__(self) -> str:
        return f"{self.name}.{self.extension}"
    

    @property
    def get_size_MB(self) -> int:
        return round(self.size/1024/1024, 2)
    
    
    @property
    def get_full_name(self) -> str:
        return f"{self.name}{self.extension}"
    
    @property
    def get_file_path(self) -> str:
        return os.path.join(settings.MEDIA_ROOT, os.path.join(f"files/",str(self.user.id), str(self.id)))

    class Meta:
        ordering = ['name']



    
