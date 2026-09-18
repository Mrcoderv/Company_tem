from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from home.sections import require_section
from .models import Post

@method_decorator(require_section('show_blog'), name='dispatch')
class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    queryset = Post.objects.filter(is_published=True).order_by('-created_at')

@method_decorator(require_section('show_blog'), name='dispatch')
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(is_published=True)
