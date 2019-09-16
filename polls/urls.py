from django.urls import path
from . import views

app_name='polls'
urlpatterns = [
    path('', views.index, name='index'),
    path('comment/', views.comment, name='comment'),
    path('comment/<int:pk>/comment_delete', views.comment_delete, name='comment_delete'),
    path('create/', views.create, name='create'),
    path('create_choice/', views.create_choice, name='create_choice'),
    path('delete/<int:pk>', views.delete, name='delete'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('detail/<int:pk>/vote/', views.vote, name='vote'),
    path('detail/<int:pk>/results/', views.results, name='results')
]