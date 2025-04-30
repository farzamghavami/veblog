from django.urls import path
from .views import Home, BlogsCreatView, BlogsListView, CommentCreate, BlogsUpdateView, BlogsDeleteView, CommentList, \
    BlogsComentsList
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', Home.as_view(), name='user-list'),
    path('blogs/', BlogsListView.as_view(), name='blog-detail'),
    path('blogs/create/', BlogsCreatView.as_view(), name='blog-list'),
    path('blogs/update/<int:pk>', BlogsUpdateView.as_view(), name='blog-update'),
    path('blogs/delete/<int:pk>', BlogsDeleteView.as_view(), name='blog-list'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('comments/', CommentList.as_view(), name='comment-list-create'),
    path('comments/create/', CommentCreate.as_view(), name='comment-list-create'),
    path('blogs/coments/<int:pk>', BlogsComentsList.as_view(), name='comment-list-create'),

]
