from .models import Category

def category_processors(request):
    return {
        'nav_categories': Category.objects.filter(published=True, featured=True)
    }

from collections import defaultdict
from .models import Post

def archive_context(request):
    archives = defaultdict(list)

    dates = Post.objects.filter(
        status=Post.Status.PUBLISHED
    ).dates('published_at', 'month', order='DESC')

    for d in dates:
        archives[d.year].append(d)

    return {'archive_years': archives}
