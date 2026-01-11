from django.contrib import admin
from .models import Category, Post, Comment, Contact

# Register your models here.
class CategoryModel(admin.ModelAdmin):
    list_display = ['name', 'slug', 'featured', 'published']
    list_filter = ['featured', 'published', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

    fieldsets = [
        ('Category Info', {'fields': ['name', 'slug', 'description']}),
        ('Other Info', {'fields': ['featured', 'published', 'created_at'], 'classes': ['collapse'], 'description': ['Optional fields']}),
        ('SEO Settings', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
                'canonical_url',
            )
        }),
        ('Open Graph', {
            'fields': (
                'og_title',
                'og_description',
                # 'og_image',
            )
        }),
    ]

admin.site.register(Category, CategoryModel)

class PostModel(admin.ModelAdmin):
    list_display = ['title', 'featured', 'status', 'category', 'author', 'created_at']
    list_filter = ['status', 'featured', 'published_at']
    search_fields = ['slug', 'content']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 3

    fieldsets = [
        ('Post Info', {'fields': ['title', 'slug', 'content']}),
        ('Other Info', {'fields': ['featured', 'status', 'category', 'author']}),
        ('Datetime', {'fields': ['created_at', 'updated_at', 'published_at']}),
        ('SEO Settings', {
            'fields': (
                'meta_title',
                'meta_description',
                'meta_keywords',
                'canonical_url',
            )
        }),
        ('Open Graph', {
            'fields': (
                'og_title',
                'og_description',
                # 'og_image',
            )
        }),
    ]

admin.site.register(Post, PostModel)

class CommentModel(admin.ModelAdmin):
    list_display = ['name', 'text', 'published']
    list_filter = ['post', 'created_at']
    search_fields = ['name', 'text', 'post']
    readonly_fields = ['created_at']

    fieldsets = [
        ('Comment Info', {'fields': ['name', 'post', 'text']}),
        ('Other Info', {'fields': ['published', 'created_at']}),
    ]

admin.site.register(Comment, CommentModel)

class ContactModel(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']
    list_filter = ['created_at']
    search_fields = ['name', 'message']
    readonly_fields = ['created_at']

    fieldsets = [
        ('Contact Info', {'fields': ['name', 'email', 'message']}),
        ('Other Info', {'fields': ['created_at'], 'classes': ['collapse']}),
    ]

admin.site.register(Contact, ContactModel)