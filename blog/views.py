from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import User, Blog, Comment
from .serializers import UserSerializer, BlogSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from permissions.permissions import IsOwnerOrAdmin




# ---------------- User ----------------
#this is for adding description for fields like search, ordering and pagination
@extend_schema(
    tags=["Users"],
    parameters=[
        OpenApiParameter(
            name="is_active",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="filter for active users",
        ),
        OpenApiParameter(
            name="is_staff",
            type=OpenApiTypes.BOOL,
            location=OpenApiParameter.QUERY,
            description="filter for staff users(true or false)",
        ),
        OpenApiParameter(
            name="search",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="search by username, email,date joined",
        ),
        OpenApiParameter(
            name="ordering",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.QUERY,
            description="ordering by username, email and date joined)",
        ),
    ],
)

@extend_schema(
    tags=["Users"])
class UserList(ListAPIView):
    """
    user list
    """

    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "is_staff"]
    search_fields = ["username", "email", "first_name", "last_name"]
    ordering_fields = ["username", "email", "date_joined"]


@extend_schema(
    tags=["Users"])
class UserDetailView(APIView):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = UserSerializer

    def get(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

@extend_schema(
    tags=["Users"])
class UserCreateView(APIView):
    """
    regitster new user
    """
    serializer_class = UserSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(
    tags=["Users"])
class UserUpdateView(APIView):
    """
    update user
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = UserSerializer
    def put(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Users"])
class UserDelete(APIView):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = UserSerializer

    def delete(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)
        user.is_active = False
        user.save()
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)



# ---------------- Blog ----------------

@extend_schema(
    tags=["blog"])
class BlogsListView(ListAPIView):
    """
    get all blogs
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = BlogSerializer

    queryset = Blog.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title","author"]
    ordering_fields = ["created_at"]



@extend_schema(
    tags=["blog"])
class BlogsCreatView(APIView):
    """
    create blog
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        current_user = get_current_user_from_token(request)
        if serializer.is_valid():
            serializer.save(author=current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["blog"])
class BlogsUpdateView(APIView):
    """
    update blog
    """
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = BlogSerializer

    def put(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        self.check_object_permissions(request, blog)
        serializer = self.serializer_class(blog, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save(author = blog.author)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["blog"])
class BlogsDeleteView(APIView):
    """
    delete blog
    """
    permission_classes = [IsOwnerOrAdmin, ]
    serializer_class = BlogSerializer

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        self.check_object_permissions(request, blog)
        blog.is_active = False
        blog.save()
        serializer = self.serializer_class(blog)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=["comments"])
class CommentList(APIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self,request):
        comment = Comment.objects.all()
        serializer_data = self.serializer_class(comment, many=True)
        return Response(serializer_data.data,status=status.HTTP_200_OK)


@extend_schema(
    tags=["comments"])
class CommentCreate(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer_data = self.serializer_class(data=request.data)
        current_user = get_current_user_from_token(request)
        if serializer_data.is_valid():
            serializer_data.save(author=current_user)
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentUpdate(APIView):
    permissions_classes = [IsOwnerOrAdmin]
    serializer_class = CommentSerializer
    def put(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        self.check_object_permissions(request, comment)
        serializer = self.serializer_class(comment, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDelete(APIView):
    permission_classes = [IsOwnerOrAdmin]
    serializer_class = CommentSerializer
    def delete(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.is_active = False
        comment.save()
        serializer = self.serializer_class(comment)

@extend_schema(
    tags=["comments"])
class CommentListView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer

    def get(self, request):
        comments = Comment.objects.all()
        serializer_data = CommentSerializer(comments, many=True)
        return Response(serializer_data.data)

@extend_schema(
    tags=["comments"])
class BlogsCommentListView(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer
    def get(self, request,pk):
        blog = get_object_or_404(Blog, pk=pk)
        coments = Comment.objects.filter(post=blog)
        serializer_data = CommentSerializer(coments, many=True)
        return Response(serializer_data.data)




def get_current_user_from_token(request):
    # استخراج توکن از header
    auth_header = request.headers.get('Authorization')

    if not auth_header or not auth_header.startswith('Bearer '):
        raise AuthenticationFailed('توکن یافت نشد یا فرمت اشتباه است.')

    token = auth_header.split(' ')[1]

    try:
        # دیکود کردن توکن با secret key
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get('user_id')

        if user_id is None:
            raise AuthenticationFailed('توکن معتبر نیست.')

        try:
            user = User.objects.get(id=user_id)
            return user

        except User.DoesNotExist:
            raise AuthenticationFailed('کاربر یافت نشد.')

    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('توکن منقضی شده.')

    except jwt.InvalidTokenError:
        raise AuthenticationFailed('توکن نامعتبر است.')
