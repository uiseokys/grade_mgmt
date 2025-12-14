from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("students/<int:pk>/", views.student_detail, name="student_detail"),
    path("students/manage/new/", views.student_create, name="student_create"),
    path("students/manage/<int:pk>/edit/", views.student_edit, name="student_edit"),

    path("subjects/", views.subject_manage, name="subject_manage"),
    path("subjects/<int:pk>/", views.subject_detail, name="subject_detail"),
    path("subjects/<int:pk>/delete/", views.subject_delete, name="subject_delete"),
]
