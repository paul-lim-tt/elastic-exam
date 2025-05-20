import logging

from django.db import models

from appdemo.models.base import BaseAutoDate, BaseUUID

logger = logging.getLogger(__name__)


class Resource(BaseUUID, BaseAutoDate):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
