
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("users/<int:user_id>/profil", views.user_detail_profil, name="user_detail_profil"),
    path("users/following", views.following_page, name="following_page"),
    path("posts", views.add_post, name="add_post"), 
    # my APIs
    path("posts/<int:post_id>/", views.post_detail, name="post_detail"),
    path("users/<int:user_id>", views.user_detail, name="user_detail"), 
    path("comments/<int:post_id>", views.comments_list, name="comments_list"), 

]
