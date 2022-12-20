from django.urls import path,include
from . import views

app_name = 'blog'

urlpatterns = [
    path('blog',views.blog,name='blog'),
    path('blog_create',views.BlogCreate.as_view(),name='create'),
    path('blog_detail/<int:pk>',views.BlogDetail.as_view(),name='detail'),
    path('blog_edit/<int:pk>',views.BlogEdit.as_view(),name='edit'),
    path('blog_delete/<int:pk>',views.BlogDelete.as_view(),name='delete'),
    path('comment/create/<int:pk>',views.CommentCreate.as_view(),name='comment'),
    # path('comment/delete/<int:pk>',views.CommentDelete.as_view(),name='comment_delete'),
    path('comment/delete/<int:pk>',views.delete_comment,name='comment_delete'),
    path('like',views.like,name='like'),
]