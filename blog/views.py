from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import User, Blog, Comment
from .serializers import UserSerializer, BlogSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.views import obtain_auth_token


# ---------------- User ----------------
class Home(APIView):
    """
    for create and list of users
    """
    serializer_class = UserSerializer
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Blog ----------------
class BlogsListView(APIView):
    """
    get all blogs
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = BlogSerializer

    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)


class BlogsCreatView(APIView):
    """
    create new blog
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BlogSerializer

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        current_user = get_current_user_from_token(request.data)
        if serializer.is_valid():
            serializer.save(author=current_user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogsUpdateView(APIView):
    """
    update blog
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = BlogSerializer

    def put(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        serializer = BlogSerializer(instance=blog, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class BlogsDeleteView(APIView):
    """
    delete blog
    """
    permission_classes = [IsAuthenticated, ]
    serializer_class = BlogSerializer

    def delete(self, request, pk):
        blog = Blog.objects.get(pk=pk)
        blog.is_active = False
        blog.save()
        serializer = BlogSerializer(blog)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

class CommentList(APIView):

    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def get(self):
        comment = Comment.objects.all()
        serializer_data = CommentSerializer(comment, many=True)
        return Response(serializer_data.data)



class CommentCreate(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer_data = CommentSerializer(data=request.data)
        current_user = get_current_user_from_token(request.data)
        if serializer_data.is_valid():
            serializer_data.save(author=current_user)
            return Response(serializer_data.data, status=status.HTTP_201_CREATED)
        return Response(serializer_data.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentList(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer

    def get(self, request):
        comments = Comment.objects.all()
        serializer_data = CommentSerializer(comments, many=True)
        return Response(serializer_data.data)

class BlogsComentsList(APIView):
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer
    def get(self, request,pk):
        blog = Blog.objects.get(pk=pk)
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
