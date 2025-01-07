from http.client import CREATED

from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import generics, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from app.models import Category, Task
from app.serializers import RegisterSerializer, UserSerializer, LoginSerializer, CategorySerializer, TaskSerializer


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
    page_size = 10


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Category viewset
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        queryset = Category.objects.all()
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
    queryset = Task.objects.all()
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        queryset = Task.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
