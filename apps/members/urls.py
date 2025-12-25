from django.urls import path
from . import views

app_name = 'members'

urlpatterns = [
    # Организации
    path('organizations/', views.organization_list_view, name='organization_list'),
    path('organizations/create/', views.create_organization_view, name='create_organization'),
    path('organizations/<uuid:org_id>/', views.organization_detail_view, name='organization_detail'),
    # Подразделения
    path('departments/', views.department_list_view, name='department_list'),
    path('departments/create/', views.create_department_view, name='create_department'),
    path('departments/<uuid:dept_id>/', views.department_detail_view, name='department_detail'),
    # Сотрудники
    path('employees/', views.employee_list_view, name='employee_list'),
    path('employees/create/', views.create_employee_view, name='create_employee'),
    path('employees/<uuid:emp_id>/', views.employee_detail_view, name='employee_detail'),
    path('employees/<uuid:emp_id>/edit/', views.edit_employee_view, name='edit_employee'),
    path('employees/<uuid:emp_id>/delete/', views.delete_employee_view, name='delete_employee'),
    # Дети сотрудников
    path('employees/<uuid:emp_id>/children/create/', views.create_child_view, name='create_child'),
    path('children/<uuid:child_id>/edit/', views.edit_child_view, name='edit_child'),
    path('children/<uuid:child_id>/delete/', views.delete_child_view, name='delete_child'),
    # Поиск и фильтрация
    path('search/', views.employee_search_view, name='employee_search'),
]