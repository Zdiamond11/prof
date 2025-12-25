from django.urls import path
from . import views

app_name = 'protocols'

urlpatterns = [
    # Собрания
    path('meetings/', views.meeting_list_view, name='meeting_list'),
    path('meetings/create/', views.create_meeting_view, name='create_meeting'),
    path('meetings/<uuid:meeting_id>/', views.meeting_detail_view, name='meeting_detail'),
    path('meetings/<uuid:meeting_id>/edit/', views.edit_meeting_view, name='edit_meeting'),
    # Мотивированные мнения
    path('motivated-opinions/', views.motivated_opinion_list_view, name='motivated_opinion_list'),
    path('motivated-opinions/create/', views.create_motivated_opinion_view, name='create_motivated_opinion'),
    path('motivated-opinions/<uuid:opinion_id>/', views.motivated_opinion_detail_view, name='motivated_opinion_detail'),
    path('motivated-opinions/<uuid:opinion_id>/edit/', views.edit_motivated_opinion_view, name='edit_motivated_opinion'),
    # Подписи документов
    path('sign-document/', views.sign_document_view, name='sign_document'),
    path('my-signed-documents/', views.my_signed_documents_view, name='my_signed_documents'),
]