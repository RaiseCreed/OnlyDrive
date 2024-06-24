from .models import Folder, File
from rest_framework import serializers



class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = ['id','name','created','files_count']


class FileSerializer(serializers.ModelSerializer):
    
    name = serializers.SerializerMethodField('return_full_name')

    def return_full_name(self, obj):
        return f'{obj.name}{obj.extension}'
    
    class Meta:
        model = File
        exclude = ['content','user','extension']

    