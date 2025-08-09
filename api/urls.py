from django.urls import path
from . import views

urlpatterns = [
    # fetch all students
    path('students/', views.studentsView),
    # fetch a single student
    path('students/<int:pk>/', views.studentDetailView),

    # class based views need .as_view()
    path('employees/', views.Employees.as_view()),
    path('employees/<int:pk>/', views.EmployeeDetail.as_view()),

]