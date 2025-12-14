from django import forms
from django.forms import formset_factory
from .models import Student, Subject, Enrollment

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["student_no", "name", "department", "gender"]
        widgets = {
            "student_no": forms.TextInput(attrs={"class":"input"}),
            "name": forms.TextInput(attrs={"class":"input"}),
            "department": forms.TextInput(attrs={"class":"input"}),
            "gender": forms.Select(attrs={"class":"input"}),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "professor", "textbook", "schedule"]
        widgets = {f: forms.TextInput(attrs={"class":"input"}) for f in fields}

class ScoreRowForm(forms.Form):
    subject_id = forms.IntegerField(widget=forms.HiddenInput())
    subject_name = forms.CharField(disabled=True, required=False)
    score = forms.IntegerField(min_value=0, max_value=100, required=True)

ScoreFormSet = formset_factory(ScoreRowForm, extra=0)
