"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from src.shops.views import ShopViewSet
from src.users.views import ProfileViewSet, user_login_view, user_logout_view, AuthViewSet, verify_forgot_password

schema_view = get_schema_view(
    openapi.Info(
        title="Marvel API",
        default_version='v1.0',
        description="Ecommerce API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('src.users.urls')),

    path('api/token/', user_login_view, name='user_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', user_logout_view, name='user_logout'),
    path('api/forgot_password/<uidb64>/<token>/', verify_forgot_password, name='verify_forgot_password'),

    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

profile_router = DefaultRouter()
profile_router.register(r'api/profiles', ProfileViewSet, basename='profile')
urlpatterns += profile_router.urls

auth_router = DefaultRouter()
auth_router.register(r'api', AuthViewSet, basename='auth')
urlpatterns += auth_router.urls

shop_router = DefaultRouter()
shop_router.register(r'api/shops', ShopViewSet, basename='shop')
urlpatterns += shop_router.urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
