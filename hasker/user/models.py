import time
from hashlib import md5

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.templatetags.static import static
from PIL import Image


def user_photo_path(instance, filename):
    name, sep, ext = filename.rpartition(".")
    if not sep:
        ext = ".jpg"
    new_filename = md5(str(time.time()).encode("utf-8")).hexdigest()
    return f"{new_filename}.{ext}"


def user_photo_size_validator(photo):
    max_size = 1
    if photo.size > max_size * 1024 * 1024:
        raise ValidationError(f"The maximum file size is {max_size}MB")
    return photo


class User(AbstractUser):
    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=50, blank=False, unique=True)
    photo = models.ImageField(
        blank=True,
        upload_to=user_photo_path,
        validators=[user_photo_size_validator],
    )
    thumb = models.ImageField(blank=True, editable=False, upload_to=user_photo_path)

    def save(self, *args, **kwargs):
        if self.photo and self._state.adding:
            self.create_thumbnail()
        super().save(*args, **kwargs)

    def create_thumbnail(self, save=False):
        content = ContentFile(b"")
        with Image.open(self.photo) as img:
            img.thumbnail((150, 150))
            img.convert(mode="RGB").save(content, format="JPEG")

        self.thumb = InMemoryUploadedFile(
            content, None, "temp.jpg", "image/jpeg", len(content), None
        )
        if save:
            self.save(update_fields=["thumb"])

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return static("media/user.png")

    def get_thumb_url(self):
        if self.thumb:
            return self.thumb.url
        return self.get_photo_url()
