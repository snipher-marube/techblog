from django.db import models
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify

class PublishedManager(models.Manager):
    """
    Custom manager to filter published posts and optimize queryset performance
    """
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(status='published')
    
class Post(models.Model):
    """
    Blog post model with optimized field configuration and search-friendly structure
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, editable=False)  # Slug generated on save
    intro = models.TextField(help_text="Brief summary for search engine snippets")
    image = models.ImageField(
        upload_to='uploads/%Y/%m/%d/',
        width_field='image_width',
        height_field='image_height',
        help_text="Web-optimized image in JPEG/WebP format"
    )
    image_width = models.IntegerField(editable=False)
    image_height = models.IntegerField(editable=False)
    body = RichTextUploadingField()
    publish = models.DateTimeField(default=timezone.now, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()  # Default manager
    published = PublishedManager()  # Custom manager for published posts

    class Meta:
        ordering = ('-publish',)
        indexes = [
            models.Index(fields=['status', 'publish']),  # Composite index for common filters
        ]
        
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        """Auto-generate slug and optimize image metadata on save"""
        if not self.slug:
            self.slug = slugify(self.title)[:255]
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Canonical URL with date-based structure for SEO"""
        return reverse('post_detail', args=[
            self.publish.year,
            self.publish.month,
            self.publish.day,
            self.slug
        ])