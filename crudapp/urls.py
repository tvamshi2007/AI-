from django.urls import path

from . import views

app_name = 'crudapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_student, name='add'),
    path('edit/<int:pk>/', views.edit_student, name='edit'),
    path('delete/<int:pk>/', views.delete_student, name='delete'),
]
