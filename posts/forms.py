from django import forms


class CreatePostForm(forms.Form):
    text = forms.CharField(max_length=500, widget=forms.Textarea)
    image = forms.ImageField(required=False)
