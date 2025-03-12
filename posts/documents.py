from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Post
from bs4 import BeautifulSoup  # For HTML stripping

@registry.register_document
class PostDocument(Document):
    """
    Elasticsearch document mapping with optimized text analysis and HTML processing
    """
    title = fields.TextField(
        analyzer='english',
        fields={'keyword': fields.KeywordField()}
    )
    body = fields.TextField(analyzer='english')
    intro = fields.TextField(analyzer='english')
    
    class Index:
        name = 'posts'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'refresh_interval': '30s'  # Balance between freshness and performance
        }
        
    class Django:
        model = Post
        fields = ['publish', 'status']
        related_models = []

    def prepare_body(self, instance):
        """Strip HTML tags and normalize whitespace for better indexing"""
        soup = BeautifulSoup(instance.body, 'html.parser')
        return ' '.join(soup.stripped_strings)