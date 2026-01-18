from django.shortcuts import render, get_object_or_404
from .models import Category, Post, Comment, Contact
from django.views.generic import ListView, DetailView, FormView, CreateView
from .forms import CommentForm, ContactForm
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
from django.db.models import Prefetch

# Create your views here.
class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'blog/home.html'
    paginate_by = 2

    def get_queryset(self):
        return Post.objects.filter(status='P', featured=True).select_related('category', 'author')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'MyBlog | Latest Post'
        return context
    
class PostDetailView(DetailView):
    model = Post
    slug_field = 'slug'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        return Post.objects.filter(status='P').select_related('category', 'author').prefetch_related('comments')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.title} | MyBlog'
        context['form'] = CommentForm()
        return context

class CategoryDetailView(DetailView):
    model = Category
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'
    context_object_name = 'category'
    template_name = 'blog/category_detail.html'
    paginate_by = 2

    def get_queryset(self):
        return Category.objects.filter(published=True).prefetch_related(
                Prefetch(
                    'posts',
                    queryset=Post.objects.select_related('category', 'author')
                )
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.object.description} - {self.object.meta_title} | MyBlog'
        posts = self.object.posts.filter(status=Post.Status.PUBLISHED, featured=True)

        paginator = Paginator(posts, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['posts'] = page_obj
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['paginator'] = paginator

        return context

class CommentView(SuccessMessageMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/post_detail.html'
    success_message = "Thank you %(name)s! Your comment send successfully."

    def dispatch(self, request, *args, **kwargs):
        self.blog_post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('blog:post-detail',
            kwargs={
                'category_slug':self.blog_post.category.slug,
                'post_slug': self.blog_post.slug,
            }
        )
    
    def form_valid(self, form):
        form.instance.post = self.blog_post
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.blog_post.title} | MyBlog'
        context['post'] = self.blog_post
        context['form'] = CommentForm()
        return context 

class ContactView(SuccessMessageMixin, FormView):
    template_name = 'blog/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('blog:contact')
    success_message = "Thank you %(name)s (%(email)s)! We will contact you soon."

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact With Us | MyBlog'
        return context

class PostSearch(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'post_list'
    paginate_by = 2

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) |
                Q(slug__icontains=query) |
                Q(category__name__icontains=query) |
                Q(author__username__icontains=query) |
                Q(content__icontains=query),
                status=Post.Status.PUBLISHED
            )
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['title'] = f'Search result for {context['query']}'
        return context

class PostYearArchiveView(YearArchiveView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    date_field = 'published_at'
    make_object_list = True
    allow_future = False
    template_name = 'blog/post_archive_year.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['title'] = f'Archive Post - {self.kwargs['year']}'
        return context

class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    date_field = 'published_at'
    allow_future = False
    template_name = 'blog/post_archive_month.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['title'] = f'Archive Post - {self.kwargs['year']}/{self.kwargs['month']}'
        return context

class PostDayArchiveView(DayArchiveView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    date_field = 'published_at'
    allow_future = False
    template_name = 'blog/post_archive_day.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['day'] = self.kwargs['day']
        context['title'] = f'Archive Post - {self.kwargs['year']}/{self.kwargs['month']}/{self.kwargs['day']}'
        return context