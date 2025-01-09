from django.urls import path
from knox import views as knox_views

from app.viewsets import SignUpAPI, SignInAPI, MainUser, CategoryViewSet, TaskViewSet, UserViewSet, SharedTaskViewSet, \
    AllCategoryViewSet

urlpatterns = []

urlpatterns += [
    path('auth/register/', SignUpAPI.as_view(), name="knox_register"),
    path('auth/login/', SignInAPI.as_view(), name="knox_login"),
    path('auth/user/', MainUser.as_view(), name="knox_user"),
    path('auth/logout/', knox_views.LogoutView.as_view(), name="knox_logout"),

    # add all viewsets here
    path('category/', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name="category"),
    path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name="category"),
    path('allcategories/', AllCategoryViewSet.as_view({'get': 'list'}), name='allcategories'),
    path('task/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name="task"),
    path('task/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name="task"),
    path('user/', UserViewSet.as_view({'get': 'list'}), name="user"),
    path('user/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name="user"),
    path('sharedtask/', SharedTaskViewSet.as_view({'get': 'list', 'post': 'create'}), name="sharedtask"),
    path('sharedtask/<int:pk>/', SharedTaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}),
         name="sharedtask"),

]
