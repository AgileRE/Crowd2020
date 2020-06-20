from django import forms
from .models import Project, Requirement, RequirementCategory, Comment
from tinymce import TinyMCE

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class ProjectForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )

    class Meta:
        model = Project
        fields = ('status_open', 'title', 'overview', 'content', 'thumbnail', 
        'categories')


class RequirementForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write requirement here...',
        'id': 'userrequirement',
        'rows': 2
    }), label="")
    category = forms.ChoiceField(choices=RequirementCategory.RCategories, 
        required=True, 
        label="")
    class Meta:
        model = Requirement
        fields = ('content', 'category')

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Write suggestions here...',
        'id': 'user_comment',
        'rows': 2
    }), label="")

    class Meta:
        model = Comment
        fields = ('content', )