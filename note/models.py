from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


# Create your models here.
class NoteModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, primary_key=True)
    categories = models.CharField(max_length=15, blank=True)
    date = models.DateField(auto_now_add=True)
    description = RichTextField(blank=True, null=True)


    def __str__(self):
        return self.title


class CommentModel(models.Model):
    note = models.ForeignKey(NoteModel, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class LikeModel(models.Model):
    note = models.ForeignKey(NoteModel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


