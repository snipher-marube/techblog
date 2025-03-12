# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Post
from django.utils.text import slugify

@admin.action(description='Publish selected articles')
def make_published(modeladmin, request, queryset):
    queryset.update(status='published')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface optimized for quick content management and visual preview
    """
    # Define the fields to include in the admin form (exclude slug)
    fields = ['title', 'intro', 'body', 'image', 'publish', 'status']
    
    # Display fields in the list view
    list_display = ['thumbnail', 'title', 'publish', 'status']
    list_filter = ['created', 'publish', 'status']
    search_fields = ['body', 'title']
    date_hierarchy = 'publish'
    list_display_links = ('title',)
    list_per_page = 10
    
    # Custom actions
    actions = [make_published]
    
    # Thumbnail display in the admin list view
    @admin.display(description='Thumbnail')
    def thumbnail(self, obj):
        return format_html(
            f'<img src="{obj.image.url}" width="40" height="40" loading="lazy" alt="{obj.title}">'
        )
    
    def save_model(self, request, obj, form, change):
        """
        Automatically generate the slug from the title if the post is being created.
        """
        if not obj.slug:  # Only generate slug if it doesn't exist
            obj.slug = slugify(obj.title)
        super().save_model(request, obj, form, change)