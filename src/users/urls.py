from django.urls import path

from src.users.views import user_detail_view, user_list_view, user_active_view, user_ban_view

app_name = 'users'

urlpatterns = [
    path('<int:id>/', user_detail_view, name='user-detail'),
    path('<int:id>/active/', user_active_view, name='user-active'),
    path('<int:id>/ban/', user_ban_view, name='user-ban'),
    path('', user_list_view, name='user-list'),
]
