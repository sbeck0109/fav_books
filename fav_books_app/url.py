from django.urls import path
from .import views

urlpatterns = [
    path('', views.login_reg),
    path('process_reg', views.process_reg),
    path('process_login', views.process_login),
    path('books', views.index),
    path('books/<int:user_id>/add', views.add),
    path('books/<int:book_id>', views.details),
    path('books/<int:book_id>/edit', views.edit),
    path('books/<int:book_id>/fav', views.add_to_favs),
    path('books/<int:book_id>/unfav', views.un_favs),
    path('books/<int:book_id>/delete', views.delete),
    path('fav_list', views.fav_list)


]
