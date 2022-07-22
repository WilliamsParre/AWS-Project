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

    # Blog URLs
    path('get_blog/', views.get_blog, name="get_blog"),
    path('my_blogs/', views.my_blogs, name="my_blogs"),
    path('add_blog/', views.add_blog, name="add_blog"),
    path('likes/<str:pk>/', views.like, name="like"),
    path('share/<str:pk>/', views.share, name="add_blog"),
    path('publish_blog/<str:pk>/', views.publish_blog, name="publish_blog"),
    path('unpublish_blog/<str:pk>/', views.unpublish_blog, name="unpublish_blog"),
    path('edit_blog/<str:pk>/', views.edit_blog, name="edit_blog"),
    path('delete_blog/<str:pk>/', views.delete_blog, name="delete_blog")
]
