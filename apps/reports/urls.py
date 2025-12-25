from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Отчеты по членству
    path('membership/', views.membership_reports_list_view, name='membership_reports_list'),
    path('membership/create/', views.create_membership_report_view, name='create_membership_report'),
    path('membership/<uuid:report_id>/download/', views.download_membership_report_view, name='download_membership_report'),
    # Демографические отчеты
    path('demographic/', views.demographic_reports_list_view, name='demographic_reports_list'),
    path('demographic/create/', views.create_demographic_report_view, name='create_demographic_report'),
    path('demographic/<uuid:report_id>/download/', views.download_demographic_report_view, name='download_demographic_report'),
    # Отчеты по движению сотрудников
    path('movement/', views.movement_reports_list_view, name='movement_reports_list'),
    path('movement/create/', views.create_movement_report_view, name='create_movement_report'),
    path('movement/<uuid:report_id>/download/', views.download_movement_report_view, name='download_movement_report'),
]