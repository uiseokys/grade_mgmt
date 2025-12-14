from django.contrib import admin
from .models import Student, Subject, Enrollment

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("student_no", "name", "department", "gender")

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "professor", "textbook", "schedule")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "score")
    list_filter = ("subject",)
