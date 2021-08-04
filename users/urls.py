from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.user_login_view, name='user_login_view'),
    path('logout/', views.user_logout_view, name='user_logout_view'),
    path('profile/', views.user_home_page_view, name='user_home_page_view')
]