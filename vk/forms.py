from django.forms import forms


class UploadPhotoForm(forms.Form):
    avatar = forms.ImageField()
