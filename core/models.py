from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ("M", "남"),
        ("F", "여"),
    ]

    student_no = models.CharField("학번", max_length=20, unique=True)
    name = models.CharField("이름", max_length=30)
    department = models.CharField("학과", max_length=50)
    gender = models.CharField("성별", max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.student_no})"

class Subject(models.Model):
    name = models.CharField("과목명", max_length=100, unique=True)
    professor = models.CharField("담당교수", max_length=50, blank=True)
    textbook = models.CharField("교재명", max_length=100, blank=True)
    schedule = models.CharField("수업시간", max_length=100, blank=True)

    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="enrollments")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="enrollments")
    score = models.PositiveSmallIntegerField("성적", default=0)

    class Meta:
        unique_together = ("student", "subject")

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}: {self.score}"
