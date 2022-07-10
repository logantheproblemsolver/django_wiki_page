from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("createnew", views.create_new_wiki, name="create")
]

handler404 = "encyclopedia.views.not_found"