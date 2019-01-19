from django import forms
from feedback.models import Question, Profile


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['description', 'type', 'section']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
