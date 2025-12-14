from django.db import transaction
from .models import Student, Subject, Enrollment

DEFAULT_SUBJECTS = [
    ("객체지향 프로그래밍", "홍길동", "OOP 교재", "월 2-3교시"),
    ("인터넷프로그래밍", "김교수", "Web 교재", "화 3-4교시"),
    ("데이터 베이스", "이교수", "DB 교재", "수 1-2교시"),
    ("분산처리기초", "박교수", "Distributed 교재", "목 4-5교시"),
]

DEFAULT_STUDENTS = [
    ("20304543", "태조", "데이터사이언스", "M"),
    ("20304544", "정조", "컴퓨터공학", "M"),
    ("20304545", "대정", "정보통신공학", "M"),
    ("20304546", "세종", "컴퓨터공학", "M"),
    ("20304547", "문종", "소프트웨어학", "M"),
    ("20304548", "단종", "데이터사이언스", "M"),
    ("20304549", "세조", "컴퓨터공학", "M"),
    ("20304550", "예종", "정보통신공학", "M"),
    ("20304551", "성종", "소프트웨어학", "M"),
    ("20304552", "연산군", "데이터사이언스", "M"),
]

@transaction.atomic
def ensure_seed_data():
    # 과목 생성
    for name, prof, book, sch in DEFAULT_SUBJECTS:
        Subject.objects.get_or_create(
            name=name,
            defaults={
                "professor": prof,
                "textbook": book,
                "schedule": sch,
            },
        )

    # 학생 생성
    for sno, name, dept, gender in DEFAULT_STUDENTS:
        Student.objects.get_or_create(
            student_no=sno,
            defaults={
                "name": name,
                "department": dept,
                "gender": gender,
            },
        )

    # 모든 학생 + 모든 과목 enrollment 생성
    subjects = list(Subject.objects.all())
    for s in Student.objects.all():
        for sub in subjects:
            Enrollment.objects.get_or_create(
                student=s,
                subject=sub,
                defaults={"score": 0},
            )


@transaction.atomic
def add_subject_and_apply_to_all(subject: Subject):
    for s in Student.objects.all():
        Enrollment.objects.get_or_create(
            student=s,
            subject=subject,
            defaults={"score": 0},
        )


@transaction.atomic
def add_student_and_apply_subjects(student: Student):
    for sub in Subject.objects.all():
        Enrollment.objects.get_or_create(
            student=student,
            subject=sub,
            defaults={"score": 0},
        )
