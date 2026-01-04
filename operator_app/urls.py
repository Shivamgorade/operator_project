from django.urls import path
from .views import (
    operator_form,
    dashboard,
    download_operator_excel,
    edit_operator,
    admin_login_view,
    admin_logout
)

urlpatterns = [
    path('', operator_form, name='operator_form'),
    path('dashboard/', dashboard, name='dashboard'),
    path('download-excel/', download_operator_excel, name='download_excel'),
    path('edit/<int:row_index>/', edit_operator, name='edit_operator'),
    path('admin-login/', admin_login_view, name='admin_login'),
    path('admin-logout/', admin_logout, name='admin_logout'),
]
