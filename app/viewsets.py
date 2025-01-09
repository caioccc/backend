from http.client import CREATED

from django.contrib.auth.models import User
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import generics, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from app.models import Category, Task, SharedTask
from app.serializers import RegisterSerializer, UserSerializer, LoginSerializer, CategorySerializer, TaskSerializer, \
    SharedTaskSerializer


class SignUpAPI(generics.GenericAPIView):
    """
    Register API endpoint.
    """
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token[1]
        }, status=CREATED)


class SignInAPI(generics.GenericAPIView):
    """
    Login API endpoint.
    """
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


class MainUser(generics.RetrieveAPIView):
    """
    Get user API endpoint.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ResultsSetPagination(PageNumberPagination):
    page_size = 5


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category viewset
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CategorySerializer
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user)
        # name = self.kwargs.get('name', None)
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class TaskViewSet(viewsets.ModelViewSet):
    """
    Task viewset
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = TaskSerializer
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        queryset = Task.objects.filter(user=self.request.user).order_by('status', '-created_at', )

        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class UserViewSet(viewsets.ModelViewSet):
    """
    User viewset
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class SharedTaskViewSet(viewsets.ModelViewSet):
    """
    Shared task viewset
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = SharedTaskSerializer
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        queryset = SharedTask.objects.filter(user=self.request.user).order_by('status', '-created_at',)
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(task__name=name)
        return queryset

