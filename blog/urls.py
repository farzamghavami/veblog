from django.urls import path
from .views import UserList, UserDelete, UserDetailView, UserCreateView, BlogsCreatView, BlogsListView, CommentCreate, \
    BlogsUpdateView, \
    BlogsDeleteView, CommentList, \
    BlogsCommentListView, UserUpdateView, CommentUpdate, CommentDelete

urlpatterns = [

    #urls for users crud
    path('register/', UserCreateView.as_view(), name='user-create'),
    path('users', UserList.as_view(), name='user-list'),
    path('user/detail/<int:pk>',UserDetailView.as_view(), name='user-detail'),
    path('user/update/<int:pk>', UserUpdateView.as_view(), name='user-update'),
    path('user/delete/<int:pk>', UserDelete.as_view(), name='user-delete'),

    #urls for blogs
    path('blogs/', BlogsListView.as_view(), name='blog-list'),
    path('blogs/create/', BlogsCreatView.as_view(), name='blog-create'),
    path('blogs/update/<int:pk>', BlogsUpdateView.as_view(), name='blog-update'),
    path('blogs/delete/<int:pk>', BlogsDeleteView.as_view(), name='blog-delete'),

    #urls for comment
    path('comments/', CommentList.as_view(), name='comment-list'),
    path('comments/create/', CommentCreate.as_view(), name='comment-create'),
    path('comments/update/<int:pk>', CommentUpdate.as_view(), name='comment-update'),
    path('comments/delete/<int:pk>', CommentDelete.as_view(), name='comment-delete'),
    path('blogs/coments/<int:pk>', BlogsCommentListView.as_view(), name='comment-blog-list'),

]
