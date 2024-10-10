from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'recipe'

urlpatterns = [
    # Post views
    path('', views.post_list, name='post_list'),
    # path('', views.PostListView.as_view(), name='post_list'),
    path('create/', views.create_recipe, name='create_recipe'),
    path('edit/<int:year>/<int:month>/<int:day>/<slug:post>/', views.edit_recipe, name='edit_recipe'),
    path(
        'tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'
    ),
    path(
        '<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'
    ),
    path('rate/<int:post_id>/', views.rate_post, name='rate_post'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path(
        '<int:post_id>/comment/', views.post_comment, name='post_comment'
    ),
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),

]