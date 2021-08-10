from django.urls import path

from users import views

urlpatterns = [
    # all users url

    path('', views.show_all_users_view, name='show_all_users_view'),

    # auth urls

    path('registration/', views.user_registration_view, name='user_registration_view'),
    path('login/', views.user_login_view, name='user_login_view'),
    path('logout/', views.user_logout_view, name='user_logout_view'),

    # profile urls

    path('<str:username>/', views.user_home_page_view, name='user_home_page_view'),
    path('<str:username>/edit/', views.user_profile_edit_view, name='user_profile_edit_view'),

    #subs urls

    path('subscribe/<int:user_id>/', views.subscribe_view, name='subscribe')
]