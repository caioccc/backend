from http.client import CREATED

from django.contrib.auth.models import User
from knox.auth import TokenAuthentication
from knox.models import AuthToken
from rest_framework import generics, permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from app.ipapi.ipapi import get_ip_full_data
from app.models import Category, Task, SharedTask, LocalUser, Weather
from app.serializers import RegisterSerializer, UserSerializer, LoginSerializer, CategorySerializer, TaskSerializer, \
    SharedTaskSerializer, CustomTaskSerializer, CustomSharedTaskSerializer, LocalUserSerializer, WeatherSerializer
from app.weatherapi.weatherapi import get_weather


def create_local_user(user):
    try:
        info_data = get_ip_full_data()
        local_user = LocalUser.objects.create(
            ip=info_data.get('ip'),
            country_name=info_data.get('country_name'),
            country_code=info_data.get('country_code'),
            city=info_data.get('city'),
            latitude=info_data.get('latitude'),
            longitude=info_data.get('longitude'),
            country_flag=info_data.get('location').get('country_flag'),
            user=user
        )
        return local_user
    except Exception as e:
        print(e)
        return None


def get_weather_api(user):
    try:
        local_user = LocalUser.objects.get(user=user)
        city = local_user.city
        code = local_user.country_code
        wheather_now = get_weather(city, code)
        new_weather = Weather.objects.create(
            city=city,
            source_photo=wheather_now['current']['weather_icons'][0],
            temperature=wheather_now['current']['temperature'],
            description=wheather_now['current']['weather_descriptions'][0],
            user=user
        )
        return WeatherSerializer(new_weather).data
    except Exception as e:
        print(e)
        return None


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
        create_local_user(user)

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
        dict_response = {
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1],
        }
        weather_user = get_weather_api(user)
        if weather_user:
            dict_response['weather'] = weather_user
        if LocalUser.objects.filter(user=user).exists():
            dict_response['local_user'] = LocalUserSerializer(LocalUser.objects.get(user=user)).data

        return Response(dict_response)


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


class AllCategoryViewSet(viewsets.ModelViewSet):
    """
    Category viewset
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.filter(user=self.request.user)
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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomTaskSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CustomTaskSerializer(queryset, many=True)
        return Response(serializer.data)

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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = CustomSharedTaskSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CustomSharedTaskSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = SharedTask.objects.filter(user=self.request.user).order_by('status', '-created_at', )
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(task__name__icontains=name)
        return queryset


class WeatherAPI(generics.GenericAPIView):
    """
    Wheather API endpoint.
    """

    def get(self, request):
        user = self.request.user
        query_weather = Weather.objects.filter(user=user)
        if query_weather.exists():
            return Response(WeatherSerializer(query_weather.order_by('-created_at').first()).data)
        else:
            weather_user = get_weather_api(user)
            if weather_user:
                return Response(weather_user)
            else:
                return Response({'error': 'No data found'}, status=404)
