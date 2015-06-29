from django.contrib import admin

from .models import Blogpost, Comment


class BlogpostAdmin(admin.ModelAdmin):
    fields = ('title', 'slug', 'description', 'content', 'allow_comments', 'author', 'created', 'modified')
    readonly_fields = ('slug', 'created', 'modified', 'author')


class CommentAdmin(admin.ModelAdmin):
    fields = ('blogpost', 'content', 'author', 'created', 'modified')
    readonly_fields = ('created', 'modified', 'blogpost', 'author')


admin.site.register(Blogpost, BlogpostAdmin)
admin.site.register(Comment, CommentAdmin)
