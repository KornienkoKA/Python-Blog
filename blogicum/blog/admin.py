from django.contrib import admin

from .models import Category, Comment, Location, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ('is_published',)
    list_display = ('title', 'description', 'created_at')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('name', 'is_published')
    list_display = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ('is_published', 'category')
    list_display = ('title', 'author', 'created_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['text']
    list_filter = ('post', 'author')
    list_display = ('text', 'author', 'created_at')
