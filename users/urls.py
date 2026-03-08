from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserDestroyAPIView,  # Пользователи
                         UserRetrieveAPIView, UsersListAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

router = SimpleRouter()

urlpatterns = [
    # Пользователи
    path('register/', UserCreateAPIView.as_view(permission_classes=(AllowAny,)), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    path('list/', UsersListAPIView.as_view(), name='users_list'),
    path('<int:pk>/detail/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),
] + router.urls
