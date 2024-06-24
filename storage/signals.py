from django.db.models.signals import post_save, post_delete
from . models import File
import os


def add_to_file_counter(sender, instance,created, **kwargs):

    if created:
        folder = instance.folder
        folder.files_count += 1
        folder.save()


def delete_file_from_disk(sender, instance: File, **kwargs):
    filePath = instance.get_file_path
    os.remove(filePath)



post_save.connect(add_to_file_counter, sender=File)
post_delete.connect(delete_file_from_disk, sender=File)






