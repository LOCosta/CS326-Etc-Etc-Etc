from .models import Profile, Project, Tag, Skill, Location
from django import forms


class ProjectForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('tag'),
                                          widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    skills_desired = forms.ModelMultipleChoiceField(queryset=Skill.objects.all().order_by('name'),
                                                    widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    location = forms.ModelChoiceField(queryset=Location.objects.all().order_by('country', 'state', 'city',
                                                                               'local_address'),
                                      empty_label='No Location', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Project
        fields = ['name', 'description', 'tags', 'skills_desired', 'location']


class ProfileForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    relevant_skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all().order_by('name'),
                                                     widget=forms.SelectMultiple(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['name', 'email', 'relevant_skills']

class SearchForm(forms.Form):
    skills_desired = forms.ModelMultipleChoiceField(queryset=Skill.objects.all().order_by('name'),
                                                     widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    location = forms.ModelChoiceField(queryset=Location.objects.all().order_by('country', 'state', 'city',
                                                                               'local_address'),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all().order_by('tag'),
                                                     widget=forms.SelectMultiple(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    project_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))