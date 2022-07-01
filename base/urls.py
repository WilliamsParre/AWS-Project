from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.login_page, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout_user, name="logout"),

    # Profile URLs
    path('profile/', views.user_profile, name='profile'),
    path('add_profile/', views.add_profile, name='add_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

    # Get Blog
    path('get_blog/', views.get_blog, name="get_blog")
]
