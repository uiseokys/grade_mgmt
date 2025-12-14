from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentForm, SubjectForm, ScoreFormSet
from .models import Student, Subject, Enrollment
from .services import ensure_seed_data, add_subject_and_apply_to_all, add_student_and_apply_subjects


def _sidebar_context():
    return {"students_sidebar": Student.objects.order_by("name")}


def _build_score_formset_for_student(student=None, post_data=None):
    """
    항상 '현재 존재하는 과목 목록' 기준으로 formset을 구성한다.
    - student가 있으면 기존 점수를 채워줌
    - POST면 post_data를 받아 binding
    """
    subjects = list(Subject.objects.order_by("name"))
    initial = []
    for sub in subjects:
        score = 0
        if student:
            e = Enrollment.objects.filter(student=student, subject=sub).first()
            score = e.score if e else 0
        initial.append({
            "subject_id": sub.id,
            "subject_name": sub.name,
            "score": score,
        })

    if post_data is not None:
        # POST binding
        return ScoreFormSet(post_data, prefix="scores")
    return ScoreFormSet(initial=initial, prefix="scores")


def home(request):
    ensure_seed_data()
    return render(request, "core/home.html", _sidebar_context())


def student_detail(request, pk: int):
    ensure_seed_data()
    student = get_object_or_404(Student, pk=pk)

    enrollments = (
        Enrollment.objects
        .filter(student=student)
        .select_related("subject")
        .order_by("subject__name")
    )

    avg_map = dict(
        Subject.objects.annotate(avg_score=Avg("enrollments__score"))
        .values_list("id", "avg_score")
    )

    rows = []
    for e in enrollments:
        avg_score = avg_map.get(e.subject_id) or 0
        avg_score = int(round(avg_score))

        if avg_score >= 80:
            letter = "A"
        elif avg_score >= 60:
            letter = "B"
        else:
            letter = "C"

        rows.append({
            "subject": e.subject,
            "score": e.score,
            "avg": avg_score,
            "letter": letter,
        })

    ctx = _sidebar_context() | {"student": student, "rows": rows}
    return render(request, "core/student_detail.html", ctx)


def subject_manage(request):
    ensure_seed_data()

    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save()
            add_subject_and_apply_to_all(subject)
            return redirect("subject_manage")
    else:
        form = SubjectForm()

    subjects = Subject.objects.order_by("name")
    ctx = _sidebar_context() | {"subjects": subjects, "form": form}
    return render(request, "core/subject_manage.html", ctx)


def subject_detail(request, pk: int):
    ensure_seed_data()
    subject = get_object_or_404(Subject, pk=pk)
    return render(request, "core/subject_detail.html", _sidebar_context() | {"subject": subject})


def subject_delete(request, pk: int):
    ensure_seed_data()
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    return redirect("subject_manage")


def student_manage(request):
    """
    학생정보관리:
    - 학번(student_no) 있으면 그 학생 UPDATE
    - 없으면 CREATE
    - 점수는 항상 덮어쓰기(update_or_create)
    """
    ensure_seed_data()

    if request.method == "POST":
        student_no = (request.POST.get("student_no") or "").strip()
        existing = Student.objects.filter(student_no=student_no).first() if student_no else None

        form = StudentForm(request.POST, instance=existing)
        formset = _build_score_formset_for_student(student=existing, post_data=request.POST)

        if form.is_valid() and formset.is_valid():
            student = form.save()

            add_student_and_apply_subjects(student)

            # formset.cleaned_data에는 subject_id/score가 들어있음
            for f in formset:
                sid = int(f.cleaned_data["subject_id"])
                score = int(f.cleaned_data["score"])
                Enrollment.objects.update_or_create(
                    student=student,
                    subject_id=sid,
                    defaults={"score": score},
                )

            return redirect("student_detail", pk=student.pk)

    else:
        form = StudentForm()
        formset = _build_score_formset_for_student(student=None, post_data=None)

    ctx = _sidebar_context() | {"form": form, "formset": formset}
    return render(request, "core/student_form.html", ctx)


def student_edit(request, pk: int):
    ensure_seed_data()
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        formset = _build_score_formset_for_student(student=student, post_data=request.POST)

        if form.is_valid() and formset.is_valid():
            student = form.save()
            add_student_and_apply_subjects(student)

            for f in formset:
                sid = int(f.cleaned_data["subject_id"])
                score = int(f.cleaned_data["score"])
                Enrollment.objects.update_or_create(
                    student=student, subject_id=sid, defaults={"score": score}
                )
            return redirect("student_detail", pk=student.pk)

    else:
        form = StudentForm(instance=student)
        formset = _build_score_formset_for_student(student=student, post_data=None)

    ctx = _sidebar_context() | {"form": form, "formset": formset, "student": student}
    return render(request, "core/student_form.html", ctx)
