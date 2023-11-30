import uuid
import os
from django.utils.crypto import get_random_string
from django.db import models


def upload_directory_org(instance, filename):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    file_name = get_random_string(10, chars)
    return "media/original/{0}.png".format(file_name)

def upload_directory_res(instance, filename):
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    file_name = get_random_string(10, chars)
    return "media/resultado/{0}.png".format(file_name)

class Detection(models.Model):
    id = models.UUIDField("ID", primary_key=True, default=uuid.uuid4, editable=False)
    original_image = models.ImageField("imagem original", upload_to=upload_directory_org)
    result_image = models.ImageField("imagem resultado", upload_to=upload_directory_res, null=True, blank=True)
    created_at = models.DateTimeField("criado em", auto_now_add=True)
    updated_at = models.DateTimeField("atualizado em", auto_now=True)
