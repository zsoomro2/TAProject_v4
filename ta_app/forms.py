from django import forms
from .models import Section, User

class EditSkillsForm(forms.ModelForm):
    skill = forms.BooleanField()

    class Meta:
        model = Skill


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ['section_number', 'LecLab', 'start', 'end', 'credits', 'instructor', 'ta']
