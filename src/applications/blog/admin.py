from django.contrib import admin

from applications.blog.models import Post


@admin.register(Post)
class PostAdminModel(admin.ModelAdmin):
    pass
