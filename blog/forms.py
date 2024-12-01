from django import forms
from .models import Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(
            max_length=25,
            widget=forms.TextInput(attrs={'class': "form-control border border-success p-2 mb-2 border-opacity-75",'placeholder': "John Doe"}), 
            label="Name")
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={"class": "form-control border border-success p-2 mb-2 border-opacity-75", 'placeholder': "sender@gmail.com"}),
            label="Email")
    to = forms.EmailField(
            widget=forms.EmailInput(attrs={"class": "form-control border border-success p-2 mb-2 border-opacity-75", 'placeholder': "receiver@gmail.com"}),
            label="To")
    comments = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={"class": "form-control border border-success p-2 mb-2 border-opacity-75", 'placeholder': "Your thoughts..."}), 
            label="Comment")


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ["name", "email", "body"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control border border-primary p-2 mb-2 border-opacity-75", "placeholder": "John Doe"}),
            "email": forms.EmailInput(attrs={"class": "form-control border border-primary p-2 mb-2 border-opacity-75", "placeholder":"john@gmail.com"}),
            "body": forms.Textarea(attrs={"class": "form-control border border-primary p-2 mb-2 border-opacity-75", "placeholder": "Share your thoughts..."}),
        }