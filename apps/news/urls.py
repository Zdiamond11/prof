from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    # Новости
    path('', views.news_list_view, name='news_list'),
    path('category/<uuid:category_id>/', views.news_by_category_view, name='news_by_category'),
    path('<uuid:news_id>/', views.news_detail_view, name='news_detail'),
    path('create/', views.create_news_view, name='create_news'),
    path('<uuid:news_id>/edit/', views.edit_news_view, name='edit_news'),
    path('<uuid:news_id>/delete/', views.delete_news_view, name='delete_news'),
    # Комментарии
    path('<uuid:news_id>/comment/', views.add_comment_view, name='add_comment'),
]