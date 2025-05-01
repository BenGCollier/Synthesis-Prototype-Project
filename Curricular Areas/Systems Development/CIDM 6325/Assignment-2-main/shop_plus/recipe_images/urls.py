from django.urls import path

from . import views

app_name = 'recipe_images'

urlpatterns = [
    path('create/', views.recipe_image_create, name='create'),
    path(
        'detail/<int:id>/<slug:slug>/',
        views.recipe_image_detail,
        name='detail',
    ),
    path('like/', views.recipe_image_like, name='like'),
    path('', views.recipe_image_list, name='list'),
    path('ranking/', views.recipe_image_ranking, name='ranking'),
]