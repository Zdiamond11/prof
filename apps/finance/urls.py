from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    # Членские взносы
    path('membership-fees/', views.membership_fees_list_view, name='membership_fees_list'),
    path('membership-fees/create/', views.create_membership_fee_view, name='create_membership_fee'),
    path('membership-fees/<uuid:fee_id>/pay/', views.pay_membership_fee_view, name='pay_membership_fee'),
    # Заявки на выплаты
    path('support-requests/', views.support_requests_list_view, name='support_requests_list'),
    path('support-requests/create/', views.create_support_request_view, name='create_support_request'),
    path('support-requests/<uuid:request_id>/', views.support_request_detail_view, name='support_request_detail'),
    path('support-requests/<uuid:request_id>/approve/', views.approve_support_request_view, name='approve_support_request'),
    path('support-requests/<uuid:request_id>/pay/', views.pay_support_request_view, name='pay_support_request'),
    # Финансовые отчеты
    path('reports/', views.financial_reports_list_view, name='financial_reports_list'),
    path('reports/create/', views.create_financial_report_view, name='create_financial_report'),
    path('reports/<uuid:report_id>/download/', views.download_financial_report_view, name='download_financial_report'),
]