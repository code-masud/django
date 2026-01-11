from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('search/', views.PostSearch.as_view(), name="post-search"),

    path('archive/<int:year>/', views.PostYearArchiveView.as_view(), name='post_archive_year'),
    path('archive/<int:year>/<int:month>/', views.PostMonthArchiveView.as_view(month_format='%m'),name='post_archive_month'),
    path('archive/<int:year>/<int:month>/<int:day>/', views.PostDayArchiveView.as_view(month_format='%m'),name='post_archive_day'),

    path('category/<slug:category_slug>/', views.CategoryDetailView.as_view(), name='category-detail'), 
    path('post/<slug:category_slug>/<slug:post_slug>/', views.PostDetailView.as_view(), name='post-detail'),
    path('comment/<int:post_id>/', views.CommentView.as_view(), name="comment"),
]
