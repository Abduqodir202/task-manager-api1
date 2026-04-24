from django.db import models

from common.models import BaseModel


class Document(BaseModel):
    title = models.CharField(max_length=200)
    content = models.TextField()

    img = models.ImageField(upload_to='images/')
    file = models.FileField(upload_to='files/')
    video = models.FileField(upload_to='videos/')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'documents'
