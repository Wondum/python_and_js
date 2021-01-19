
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("maintain_article/<str:art_action>", views.maintain_article, name="maintain_article"),
    path("delete_article", views.delete_article, name="delete_article"),
    path("view_article/<int:id>", views.view_article, name="view_article"),
    path("author", views.author, name="author"),
    path("tag/<str:tag_name>", views.tag, name="tag"),
    path("star/<str:star_name>", views.star, name="star"),
    path("view_magazine", views.view_magazine, name="view_magazine"),
    path("manage_resource/<str:resource_name>", views.manage_resource, name="manage_resource"),

    # API Routes
    
    path("get_articles/<str:page_type>/<int:article_id>", views.get_articles, name="get_articles"),
]
