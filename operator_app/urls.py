from django.urls import path
from .views import operator_form, dashboard, download_operator_excel

urlpatterns = [
    path('', operator_form, name='operator_form'),
    path('dashboard/', dashboard, name='dashboard'),
    path('download-excel/', download_operator_excel, name='download_excel'),
]
