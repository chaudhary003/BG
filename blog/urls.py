from django.urls import path
from . import views

app_name='blog'
urlpatterns=[
path('',views.post_list,name='post_list'),
path('tag/<slug:tag_slug>/',views.post_list,name='post_list_by_tag'),
path('<int:post_id>/share/',views.post_share,name='post_share'),
path('<slug:post>',views.post_details,name='post_details')
]
