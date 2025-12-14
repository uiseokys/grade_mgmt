from django import forms
from django.forms import formset_factory
from .models import Student, Subject


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["student_no", "name", "department", "gender"]
        widgets = {
            "student_no": forms.TextInput(attrs={"class": "input"}),
            "name": forms.TextInput(attrs={"class": "input"}),
            "department": forms.TextInput(attrs={"class": "input"}),
            "gender": forms.Select(attrs={"class": "input"}),
        }


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "professor", "textbook", "schedule"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input"}),
            "professor": forms.TextInput(attrs={"class": "input"}),
            "textbook": forms.TextInput(attrs={"class": "input"}),
            "schedule": forms.TextInput(attrs={"class": "input"}),
        }


class ScoreForm(forms.Form):
    subject_id = forms.IntegerField(widget=forms.HiddenInput())
    subject_name = forms.CharField(disabled=True, required=False)
    score = forms.IntegerField(min_value=0, max_value=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["subject_name"].widget = forms.TextInput(attrs={"class": "input", "readonly": True})
        self.fields["score"].widget = forms.NumberInput(attrs={"class": "input"})


ScoreFormSet = formset_factory(ScoreForm, extra=0)
