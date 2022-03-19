from django import forms

class UploadFileForm(forms.Form):
    project_pk = forms.IntegerField(required=True)
    task_pk = forms.IntegerField(required=True)
    file = forms.FileField(required=True)