from . import views

from django.urls import path

urlpatterns = [
    path(r'user', views.user, name="user"),
    path(r'attendance', views.attendance, name="attendance"),
    path(r'student/<int:student_id>', views.student, name="student_id_lookup"),
    path(r'student', views.studentSearch, name='student'),
    path(r'plan_absence', views.plan_absence, name="planned_absence"),
    path(r'attendance-codes', views.get_attendance_codes, name="attendance-codes")
]
