from django import forms


class UploadPhotoForm(forms.Form):
    avatar = forms.ImageField()