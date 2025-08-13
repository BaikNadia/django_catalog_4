from blogs.models import BlogPost

from django.views.generic import ListView, DetailView, CreateView
from django.views.generic import UpdateView, DeleteView
from django.urls import reverse_lazy, reverse


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blogs/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)  # Только опубликованные


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/blogpost_detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views_count += 1
        self.object.save()
        return super().get(request, *args, **kwargs)


class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ('title', 'content', 'preview', 'is_published')
    success_url = reverse_lazy('blogs:blogpost_list')


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blogs/blogpost_form.html'

    def get_success_url(self):
        return reverse_lazy('blogs:blogpost_detail', kwargs={'pk': self.object.pk})



class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blogs/blogpost_confirm_delete.html'
    success_url = '/blogs/'
