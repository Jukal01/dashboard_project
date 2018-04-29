from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'create/', views.create_view, name='create'),
    url(r'list/', views.list_view, name='list'),
    url(r'(?P<id>\d+)/delete/', views.delete_view, name='delete'),
    url(r'(?P<id>\d+)/update/', views.update_view, name='update'),
]
