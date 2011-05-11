from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.finders import BaseStorageFinder
from django.conf import settings


class StaticFinder(BaseStorageFinder):
    storage = FileSystemStorage(settings.STATIC_ROOT, settings.STATIC_URL)