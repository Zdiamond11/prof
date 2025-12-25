from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    # Голосования
    path('', views.voting_list_view, name='voting_list'),
    path('create/', views.create_voting_view, name='create_voting'),
    path('<uuid:voting_id>/', views.voting_detail_view, name='voting_detail'),
    path('<uuid:voting_id>/vote/', views.vote_view, name='vote'),
    path('<uuid:voting_id>/results/', views.voting_results_view, name='voting_results'),
    # Голосования кворума
    path('quorum/', views.quorum_voting_list_view, name='quorum_voting_list'),
    path('quorum/create/', views.create_quorum_voting_view, name='create_quorum_voting'),
    path('quorum/<uuid:voting_id>/', views.quorum_voting_detail_view, name='quorum_voting_detail'),
    path('quorum/<uuid:voting_id>/vote/', views.quorum_vote_view, name='quorum_vote'),
]