from django.contrib import admin
from .models import NoteModel, CommentModel, LikeModel

admin.site.register(NoteModel)
admin.site.register(CommentModel)
admin.site.register(LikeModel)
# Register your models here.
