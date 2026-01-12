from .models import Category

def category_processors(request):
    return {
        'nav_categories': Category.objects.filter(published=True, featured=True)
    }

from django.db.models.functions import TruncYear, TruncMonth
from django.db.models import Count
from .models import Post

def archive_menu(request):
    years = (
        Post.objects
        .filter(status=Post.Status.PUBLISHED)
        .annotate(year=TruncYear("published_at"))
        .values("year")
        .annotate(total=Count("id"))
        .order_by("-year")
    )

    archive = []
    for y in years:
        months = (
            Post.objects
            .filter(
                published_at__year=y["year"].year,
                status=Post.Status.PUBLISHED
            )
            .annotate(month=TruncMonth("published_at"))
            .values("month")
            .annotate(total=Count("id"))
            .order_by("-month")
        )
        archive.append({
            "year": y["year"].year,
            "months": months
        })

    return {"archive_menu": archive}

