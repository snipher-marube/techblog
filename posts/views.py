# views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.core.cache import cache
from django_elasticsearch_dsl.search import Search

from .documents import PostDocument  # Import your document
from .models import Post
from .forms import SearchForm

def posts(request):
    """
    Paginated post list with optimized database queries and caching
    """
    cache_key = f'posts_page_{request.GET.get("page", 1)}'
    posts = cache.get(cache_key)
    
    if not posts:
        post_list = Post.published.all().only(
            'title', 'slug', 'intro', 'image', 'publish'
        )
        paginator = Paginator(post_list, 6)  # Optimal for 3-column grid
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)
        cache.set(cache_key, posts, timeout=300)  # Cache for 5 minutes
    
    return render(request, 'posts/articles.html', {'posts': posts})

def post_detail(request, year, month, day, post):
    """
    Post detail view with cached related content and optimized queries
    """
    post = get_object_or_404(Post.published, slug=post, publish__year=year,
                           publish__month=month, publish__day=day)
    
    cache_key = f'related_{post.id}'
    random_posts = cache.get(cache_key)
    
    if not random_posts:
        random_posts = Post.published.exclude(id=post.id).only(
            'title', 'slug', 'image', 'publish'
        ).order_by('?')[:6]
        cache.set(cache_key, random_posts, timeout=3600)  # Cache for 1 hour
    
    return render(request, 'posts/detail.html', {
        'post': post,
        'random_posts': random_posts
    })

def post_search(request):
    """
    Elastic-powered search with relevance sorting and query optimization
    """
    form = SearchForm(request.GET or None)
    results = []
    
    if form.is_valid():
        query = form.cleaned_data['query']
        search = PostDocument.search().query(
            'multi_match', 
            query=query,
            fields=['title^3', 'body^2', 'intro'],
            fuzziness='AUTO'
        )
        results = search.to_queryset().only(
            'title', 'slug', 'intro', 'image', 'publish'
        )
    
    return render(request, 'posts/search.html', {
        'form': form,
        'results': results,
        'query': form.cleaned_data.get('query', '')
    })