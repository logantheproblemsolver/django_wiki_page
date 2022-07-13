from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("createnew", views.create_new_wiki, name="create"),
    path("random", views.random_page, name="random"),
    path("wiki/<str:title>/edit", views.edit_wiki, name="edit"),
    path("searchwikis", views.search_page, name="search")
]

handler404 = "encyclopedia.views.not_found"