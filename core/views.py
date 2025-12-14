from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import StudentForm, SubjectForm, ScoreFormSet
from .models import Student, Subject, Enrollment
from .services import ensure_seed_data, add_subject_and_apply_to_all, add_student_and_apply_subjects


def _sidebar_context():
    return {"students_sidebar": Student.objects.order_by("name")}


def home(request):
    ensure_seed_data()
    ctx = _sidebar_context()
    return render(request, "core/home.html", ctx)


def student_detail(request, pk: int):
    ensure_seed_data()
    student = get_object_or_404(Student, pk=pk)

    # enrollments
    enrollments = (
        Enrollment.objects
        .filter(student=student)
        .select_related("subject")
        .order_by("subject__name")
    )

    # subject averages across all students
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

    ctx = _sidebar_context() | {
        "student": student,
        "rows": rows,   # ✅ 항상 성적표를 보여주기 위해 show_grades 제거
    }
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
    ctx = _sidebar_context() | {"subject": subject}
    return render(request, "core/subject_detail.html", ctx)


@require_POST
def subject_delete(request, pk: int):
    ensure_seed_data()
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()  # Enrollment도 CASCADE로 같이 삭제
    return redirect("subject_manage")


def student_create(request):
    ensure_seed_data()
    if request.method == "POST":
        form = StudentForm(request.POST)
        formset = ScoreFormSet(request.POST, prefix="scores")
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
        form = StudentForm()
        initial = []
        for sub in Subject.objects.order_by("name"):
            initial.append({"subject_id": sub.id, "subject_name": sub.name, "score": 0})
        formset = ScoreFormSet(initial=initial, prefix="scores")

    ctx = _sidebar_context() | {"form": form, "formset": formset, "mode": "create"}
    return render(request, "core/student_form.html", ctx)


def student_edit(request, pk: int):
    ensure_seed_data()
    student = get_object_or_404(Student, pk=pk)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        formset = ScoreFormSet(request.POST, prefix="scores")
        if form.is_valid() and formset.is_valid():
            student = form.save()

            # ensure enrollment exists for new subjects added later
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
        initial = []
        for sub in Subject.objects.order_by("name"):
            e = Enrollment.objects.filter(student=student, subject=sub).first()
            initial.append({
                "subject_id": sub.id,
                "subject_name": sub.name,
                "score": e.score if e else 0,
            })
        formset = ScoreFormSet(initial=initial, prefix="scores")

    ctx = _sidebar_context() | {
        "form": form,
        "formset": formset,
        "mode": "edit",
        "student": student
    }
    return render(request, "core/student_form.html", ctx)
