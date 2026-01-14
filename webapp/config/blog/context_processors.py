from .models import Category

def category_processors(request):
    return {
        'nav_categories': Category.objects.filter(published=True, featured=True)
    }

from django.db.models.functions import TruncYear, TruncMonth, TruncDay
from django.db.models import Count
from .models import Post

def archive_menu(request):
    archive = []

    years = (
        Post.objects
        .filter(status=Post.Status.PUBLISHED)
        .annotate(year=TruncYear('published_at'))
        .values('year')
        .annotate(total=Count('id'))
        .order_by('-year')
    )

    for y in years:
        month_data = []

        months = (
            Post.objects
            .filter(status=Post.Status.PUBLISHED, published_at__year=y['year'].year)
            .annotate(month=TruncMonth('published_at'))
            .values('month')
            .annotate(total=Count('id'))
            .order_by('-month')
        )

        for m in months:
            days = (
                Post.objects
                .filter(
                    status=Post.Status.PUBLISHED,
                    published_at__year=y['year'].year,
                    published_at__month=m['month'].month
                )
                .annotate(day=TruncDay('published_at'))
                .values('day')
                .annotate(total=Count('id'))
                .order_by('-day')
            )

            month_data.append({
                'month': m,
                'days': days
            })

        archive.append({
            'years': y,
            'months': month_data
        })
    return {"archive_menu": archive}
