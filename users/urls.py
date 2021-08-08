from django.urls import path

from users import views

urlpatterns = [
    # auth urls

    path('registration/', views.user_registration_view, name='user_registration_view'),
    path('login/', views.user_login_view, name='user_login_view'),
    path('logout/', views.user_logout_view, name='user_logout_view'),

    # profile urls

    path('profile/', views.user_home_page_view, name='user_home_page_view'),
    path('profile_edit/', views.user_profile_edit_view, name='user_profile_edit_view')
]