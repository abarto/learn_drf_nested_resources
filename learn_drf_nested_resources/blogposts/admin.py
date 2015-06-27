from django.contrib import admin

from .models import Blogpost, Comment


admin.site.register(Blogpost)
admin.site.register(Comment)
