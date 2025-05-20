from django.contrib import admin

from appdemo.models.container import ChunkGroup, Page
from appdemo.models.resource import Resource

# Register your models here.
admin.register(Resource)
admin.register(Page)
admin.register(ChunkGroup)
