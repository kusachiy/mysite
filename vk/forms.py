from django import forms


class UploadPhotoForm(forms.Form):
   picture = forms.ImageFields()