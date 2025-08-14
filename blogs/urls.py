from django.urls import path
from blogs.apps import BlogsConfig



from blogs.views import BlogPostListView, BlogPostUpdateView, BlogPostDetailView, BlogPostDeleteView, BlogPostCreateView

app_name = BlogsConfig.name

urlpatterns = [
    path('', BlogPostListView.as_view(), name='blogpost_list'),
    path('blogs/<int:pk>/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('blogs/create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('blogs/<int:pk>/update/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('blogs/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='blogpost_delete'),
]
