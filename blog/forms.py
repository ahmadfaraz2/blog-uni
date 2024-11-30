from django import forms

class EmailPostForm(forms.Form):
    name = forms.CharField(
            max_length=25,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "John Doe"}),
            label="Name")
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': "sender@gmail.com"}),
            label="Email")
    to = forms.EmailField(
            widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': "receiver@gmail.com"}),
            label="To")
    comments = forms.CharField(
            required=False,
            widget=forms.Textarea(attrs={"class": "form-control", 'placeholder': "Your thoughts..."}), 
            label="Comment")

