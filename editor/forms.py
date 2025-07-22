from django import forms
from .models import Document
from django.contrib.auth import get_user_model

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'content']

class FileUploadForm(forms.Form):
    file = forms.FileField()

class ShareDocumentForm(forms.Form):
    users = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple
    )
