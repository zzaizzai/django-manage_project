
from project.models import Project
from django import forms


class CreateProject(forms.From):

    class Meta:
        model = Project
        fields = ('title', 'text')

    # def __init__(self, *args, **kwargs):
    #     super(CreateProject, self).__init__(*args, **kwargs)
        
    #     for fieldname in ['username', 'password1', 'password2']:
    #         self.fields[fieldname].help_text = None
    #     # self.fields['username'].widget.attrs['class'] = 'form-control'
    #     # self.fields['password1'].widget.attrs['class'] = 'form-control'
